from django.urls import path,include
from django.conf.urls import url
from .apiviews import *

app_name = 'landingPageTester'

urlpatterns = [
    path('page/traffic/<str:url>', TrafficHistory.as_view(), name='list'),
    path('pages/', AllPagesList.as_view(), name='all')
]

# Q3rj7tG54k7EWUjZKt3Yg5lcso1jobNw7ALYRTcO
# python awis.py -u remiljw@gmail.com --key=Q3rj7tG54k7EWUjZKt3Yg5lcso1jobNw7ALYRTcO --action=urlInfo --options="&ResponseGroup=Rank&Url=sfgate.com"