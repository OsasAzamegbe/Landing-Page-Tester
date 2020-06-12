from rest_framework import  status,generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .views import  api_add, api_link, api_speed


class TrafficHistory(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrafficSerializer
    queryset = Page.objects.all()
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['url']

    def get_queryset(self):
        queryset = Page.objects.all()
        url=self.kwargs['url']
        page = queryset.filter(page_url=url)
        if page:
            return page
        else:
            api_add(url)
            return queryset.filter(page_url=url)
    
class SpeedApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SpeedSerializer
    queryset = Speed.objects.all()

    def get_queryset(self):
        queryset = Speed.objects.all()
        url_=self.kwargs['url']
        speed = queryset.filter(page_url=url_)
        if speed:
            return speed
        else:
            api_speed(url_)
            return queryset.filter(page_url=url_)

class LinkCountApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CountSerializer
    queryset = LinkCount.objects.all()

    def get_queryset(self):
        queryset = LinkCount.objects.all()
        url=self.kwargs['url']
        link = queryset.filter(page_url=url)
        if link:
            return link
        else:
            api_link(url)
            return queryset.filter(page_url=url)

    
       
class AllTrafficList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Page.objects.all()
    serializer_class = TrafficSerializer


def doc_json(request):
    return HttpResponseRedirect('/v1/documentation.json')


class ConfigureDetailsApi(APIView):
 
    def get_object(self, company_id):
        try:
            return ConfigureDetails.objects.get(company_id=company_id)
        except ConfigureDetails.DoesNotExist:
            raise Http404
 
    def post(self, request):
        serializer = ConfigureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def put(self, request):
        company_id = request.data['company_id']
        config_detail = self.get_object(company_id)
        serializer = ConfigureSerializer(config_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)