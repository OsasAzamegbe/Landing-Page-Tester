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
def index(requests):
    return render(requests, 'index.html')

@api_view(["POST"])
def TestPage(url):
    try:
        if type(url) != str:
            url = str(url)
        reply = requests.get(url)
        return JsonResponse("The status code is -", reply.status_code)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

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