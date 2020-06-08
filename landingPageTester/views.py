from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
from django.core import serializers
from django.conf import settings
import json
import requests

# Create your views here.

@api_view(["POST"])
def TestPage(url):
    try:
        if type(url) != str:
            url = str(url)
        reply = requests.get(url)
        return JsonResponse("The status code is -", reply.status_code)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
