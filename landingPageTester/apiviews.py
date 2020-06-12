from rest_framework import  status,generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect,Http404
from django.urls import reverse
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .views import  api_add, api_link, api_speed


class TrafficHistory(generics.ListAPIView):
    """
    Returns Traffic History of a particular Landing Page 
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TrafficSerializer
    queryset = Page.objects.all()


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
    """
    Returns the speed data of a particular Landing Page
    """
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
    """
    Returns the count of links clicked to get to a particular Landing Page
    """
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
    """
    Returns a list of all Landing Pages traffic in our database.
    If you can't find what you are looking for, get it via the traffic end point
    """
    permission_classes = (IsAuthenticated,)
    queryset = Page.objects.all()
    serializer_class = TrafficSerializer


def doc_json(request):
    return HttpResponseRedirect('/v1/documentation.json')





@permission_classes((AllowAny, ))
class CreateUserApi(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    def create(self, request, *args, **kwargs):     
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class ConfigureDetailsApi(generics.CreateAPIView):
    serializer_class = ConfigureSerializer

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