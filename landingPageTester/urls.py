from django.urls import path,include
from django.conf.urls import url
from .apiviews import *

app_name = 'landingPageTester'

urlpatterns = [
    path('page/(?P<url>.+)/$', PageList.as_view(), name='list'),
    path('pages/', AllPagesList.as_view(), name='all')
]