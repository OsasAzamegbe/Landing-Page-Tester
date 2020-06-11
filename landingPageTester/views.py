import base64, hashlib, hmac, os
import logging, getopt
import boto3
import getpass
import time
from configparser import ConfigParser
from future.standard_library import install_aliases
install_aliases()
from urllib.parse import parse_qs, quote_plus
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.conf import settings
from django.urls import reverse
from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from .models import Traffic, Page
<<<<<<< HEAD
=======
import tldextract
>>>>>>> development

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
    # if cur_time > exp_time:
    #     refresh_credentials(user)
    # else:
    break


# Create a date for headers and the credential string
t = datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
datestamp = t.strftime('%Y%m%d')
canonical_uri = '/api'
canonical_querystring = "Action=TrafficHistory&Range=1&ResponseGroup=History" 
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
apikey = "Q3rj7tG54k7EWUjZKt3Yg5lcso1jobNw7ALYRTcO"


def add_page(request):
    # if  request.method == 'GET':
    #     return render(request, 'index.html')
    if request.method == 'POST':
        url_check = request.POST.get('url')

        headers = {'Accept':'application/xml',
                'Content-Type': content_type,
                'X-Amz-Date':amzdate,
                'Authorization': authorization_header,
                'x-amz-security-token': session_token,
                'x-api-key': apikey}
        request_url = f"https://awis.api.alexa.com/api?{canonical_querystring}&Url={url_check}"
        r = requests.get(request_url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        status_code = soup.responsestatus.statuscode.get_text()
        rank = soup.rank.get_text()
        result_url = soup.site.get_text()
        try:
            result_page_views_permillion = soup.pageviews.permillion.get_text()
 
        except:
            result_page_views_permillion = "0.0"

        finally:
            page_domain = tldextract.extract(result_url).domain
            traffic = Page(page_url=result_url, page_name=page_domain, page_traffic=float(result_page_views_permillion), page_status=int(status_code),page_rank=rank)
            traffic_exists = Page.objects.filter(page_url=result_url).exists()
            if traffic_exists:
                Page.objects.filter(page_url=result_url).delete()
            traffic.save()
        return HttpResponseRedirect(reverse('index'))


def get_url(request,pk):
    get_url = Page.objects.get(id=pk)
    context = {
        'url':get_url
    }
    return render(request, 'edit.html', context)
def get_status(request):
    if  request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        url_check = request.POST.get('url')
    Page = Page.objects.filter(page_url=url_check)
    status = Page.page_status
    context= {
        'status': status
    }
    return render(request, 'status.html', context)    

            
def delete_page(request, pk):    
    if request.method == 'POST':
        delete_urls= Page.objects.get(id=pk)
        delete_urls.delete()
    return HttpResponseRedirect(reverse('index'))
    
def edit_url(request):
    if request.method == 'GET':
        return render(request, 'edit.html')
    
    if request.method == 'POST':
        url_check = request.POST.get('url')
        
        headers = {'Accept': 'application/xml',
                   'Content-Type': content_type,
                   'X-Amz-Date': amzdate,
                   'Authorization': authorization_header,
                   'x-amz-security-token': session_token,
                   'x-api-key': apikey}
        request_url = f"https://awis.api.alexa.com/api?{canonical_querystring}&Url={url_check}"
        r = requests.get(request_url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        status_code = soup.responsestatus.statuscode.get_text()
        rank = soup.rank.get_text()
        result_url = soup.site.get_text()
        try:
            result_page_views_permillion = soup.pageviews.permillion.get_text()
        
        except:
            result_page_views_permillion = "0.0"
        
        finally:
            page_domain = tldextract.extract(result_url).domain

            traffic = Page.objects.filter(page_url=url_check).update(page_url=result_url, page_name=page_domain,page_traffic=float(result_page_views_permillion),
                           page_status=int(status_code), page_rank=rank)
            # Page.objects.get()
            # traffic.save()
            return HttpResponseRedirect(reverse('index'))
def index(request):
    all_pages = Page.objects.all()
    context = {            
        'pages': all_pages
    }
    return render(request, 'index.html', context)


def manage(request, pk):
    page = Page.objects.get(id=pk)
    context = {            
        'page': page
    }
    return render(request, 'manage.html', context)
  
  
def api_add(url):
    url_check = url

    headers = {'Accept':'application/xml',
            'Content-Type': content_type,
            'X-Amz-Date':amzdate,
            'Authorization': authorization_header,
            'x-amz-security-token': session_token,
            'x-api-key': apikey}
    request_url = f"https://awis.api.alexa.com/api?{canonical_querystring}&Url={url_check}"
    r = requests.get(request_url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    try:
        status_code = soup.responsestatus.statuscode.get_text()
        rank = soup.rank.get_text()
        result_url = soup.site.get_text()
        result_page_views_permillion = soup.pageviews.permillion.get_text()

    except:
        result_page_views_permillion = "0.0"

    finally:
        page_domain = tldextract.extract(result_url).domain
        traffic = Page(page_url=result_url, page_name=page_domain, page_traffic=float(result_page_views_permillion), page_status=int(status_code),page_rank=rank)
        traffic_exists = Page.objects.filter(page_url=result_url).exists()
        if traffic_exists:
            Page.objects.filter(page_url=result_url).delete()
        traffic.save()


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