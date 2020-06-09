import base64, hashlib, hmac, os
import logging, getopt
import boto3
import getpass
import time
from configparser import ConfigParser
from future.standard_library import install_aliases
install_aliases()
from urllib.parse import parse_qs, quote_plus
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
from django.core import serializers
from django.conf import settings
# from . import credentials
from datetime import datetime
import json

import requests

# Create your views here.

# ************* REQUEST VALUES *************
host = 'awis.api.alexa.com'
endpoint = 'https://' + host
region = 'us-east-1'
method = 'GET'
service = 'execute-api'
log = logging.getLogger( "awis" )
content_type = 'application/xml'
local_tz = "America/Los_Angeles"
# ******** LOCAL CREDENTIALS FILE **********
credentials_file = '.awis.py.credentials'

# ******* COGNITO AUTHENTICATION  *********
cognito_user_pool_id = 'us-east-1_n8TiZp7tu'
cognito_client_id = '6clvd0v40jggbaa5qid2h6hkqf'
cognito_identity_pool_id = 'us-east-1:bff024bb-06d0-4b04-9e5d-eb34ed07f884'
cognito_region = 'us-east-1'

# refresh_credentials                                                         #
###############################################################################
def refresh_credentials(user):
    client_idp = boto3.client('cognito-idp', region_name=cognito_region, aws_access_key_id='', aws_secret_access_key='')
    client_identity = boto3.client('cognito-identity', region_name='us-east-1')

    password = 'michael89'
    response = client_idp.initiate_auth(
        ClientId=cognito_client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': 'remiljw@gmail.com',
            'PASSWORD': password
        }
    )

    idtoken = response['AuthenticationResult']['IdToken']
    response = client_identity.get_id(
        IdentityPoolId=cognito_identity_pool_id,
        Logins={
            'cognito-idp.us-east-1.amazonaws.com/'+cognito_user_pool_id: idtoken
        }
    )
    identityid = response['IdentityId']
    response = client_identity.get_credentials_for_identity(
        IdentityId=identityid,
        Logins={
            'cognito-idp.us-east-1.amazonaws.com/'+cognito_user_pool_id: idtoken
        }
    )

    config = ConfigParser()
    config['DEFAULT'] = {'aws_access_key_id': response['Credentials']['AccessKeyId'],
                         'aws_secret_access_key': response['Credentials']['SecretKey'],
                         'aws_session_token': response['Credentials']['SessionToken'],
                         'expiration': time.mktime(response['Credentials']['Expiration'].timetuple())
                        }

    print('Writing new credentials to %s\n' % credentials_file)
    with open(credentials_file, 'w') as configfile:
        config.write(configfile)
    configfile.close()

###############################################################################
# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
###############################################################################
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

###############################################################################
# sortQueryString                                                             #
###############################################################################
def sortQueryString(queryString):
    queryTuples = parse_qs(queryString)
    sortedQueryString = ""
    sep=""
    for key in sorted(queryTuples.keys()):
        sortedQueryString = sortedQueryString + sep + key + "=" + quote_plus(queryTuples[key][0])
        sep="&"
    return sortedQueryString
user = 'remiljw@gmail.com'

config = ConfigParser()
config.read(credentials_file)
if not os.path.isfile(credentials_file):
        refresh_credentials(user)
while True:

    access_key = config.get("DEFAULT", "aws_access_key_id")
    secret_key = config.get("DEFAULT", "aws_secret_access_key")
    session_token = config.get("DEFAULT", "aws_session_token")
    expiration = config.get("DEFAULT", "expiration")
    exp_time = float(expiration)
    cur_time = time.mktime(datetime.now().timetuple())
    user = "remiljw@gmail.com"
    if cur_time > exp_time:
        refresh_credentials(user)
    else:
        break


# Create a date for headers and the credential string
t = datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
datestamp = t.strftime('%Y%m%d')
canonical_uri = '/api'
canonical_querystring = "Action=TrafficHistory&Range=1ResponseGroup=History&Url=" 
canonical_querystring = sortQueryString(canonical_querystring)
canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
signed_headers = 'host;x-amz-date'
payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()
canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
signing_key = getSignatureKey(secret_key, datestamp, region, service)
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
apikey = "goo1ibDWTh4DDdacQm0xH3xtqvehKroK6OPqyMPy"


def webinfo(request):
    if  request.method == 'GET':
        url_check = request.GET.get('url')
    headers = {'Accept':'application/xml',
               'Content-Type': content_type,
               'X-Amz-Date':amzdate,
               'Authorization': authorization_header,
               'x-amz-security-token': session_token,
               'x-api-key': apikey}
    request_url = "https://https://awis.api.alexa.com/api?"+url_check
    r = requests.get(request_url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        result['success'] = True
    else:
        result['success'] = False
    return render(request, 'index.html', result)






# def index(requests):
#     return render(requests, 'index.html')

# @api_view(["POST"])
# def TestPage(url):
#     try:
#         if type(url) != str:
#             url = str(url)
#         reply = requests.get(url)
#         return JsonResponse("The status code is -", reply.status_code)
#     except ValueError as e:
#         return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

# def webinfo(request):
#     content_type = 'application/xml'
#     apikey = 'hMOokdXqvI2K7LOva7sU42YVb64oXawZ9N6ROoea'
#     access_key = 'ASIA2TRI3LACDYYL26OK'
#     t = datetime.utcnow()
#     secret_key = 'feVltyVtGpxqpYFMF+ik4dusECP8y4DhA6Eyl6mM'
#     amzdate = t.strftime('%Y%m%dT%H%M%SZ')
#     datestamp = t.strftime('%Y%m%d') 
#     region = 'us-east-1'
#     service = 'execute-api'
#     credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
#     signed_headers = 'host;x-amz-date'
#     signature = 
#     session_token = 
#      algorithm = 'AWS4-HMAC-SHA256'
#     authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
#     if request.method == 'GET':
#         url =  request.GET.get('site')
#         endpoint = 'https://ats.api.alexa.com/api?'
#         headers = {'Accept':'application/xml',
#                'Content-Type': content_type,
#                'X-Amz-Date':amzdate,
#                'Authorization': authorization_header,
#                'x-amz-security-token': session_token,
#                'x-api-key': apikey
#               }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         result = response.json()
#         result['success'] = True
#     else:
#         result['success'] = False
#     return render(request, 'index.html', result)