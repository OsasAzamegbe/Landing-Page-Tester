from rest_framework import  status,generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from .models import Page
from .serializers import landingPageSerializer
from .views import add_page, api_add


class TrafficHistory(generics.ListAPIView):
    serializer_class = landingPageSerializer
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
    

    
       
class AllPagesList(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = landingPageSerializer

# class Alexa(APIView):

#     def alexa(request, url):
#         add_page()

