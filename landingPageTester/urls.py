from django.urls import path,include
from django.conf.urls import url
from .apiviews import * 
from rest_framework.authtoken.views import obtain_auth_token

# from rest_framework_simplejwt import views as jwt_views

app_name = 'landingPageTester'

urlpatterns = [
	# path('token/', jwt_views.TokenObtainPairView.as_view(), name='token-obtain'),
	# path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token-refresh'),
    path('traffic/<path:url>', TrafficHistory.as_view(), name='traffic'),
    path('speed/<path:url>', SpeedApi.as_view(), name='speed'),
    path('count/<path:url>', LinkCountApi.as_view(), name='count'),
    path('alltraffic/', AllTrafficList.as_view(), name='all'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('documentation/', doc_json, name='documentation'),
    path('configure/', ConfigureDetailsApi.as_view(), name='configuration'),
]

# Q3rj7tG54k7EWUjZKt3Yg5lcso1jobNw7ALYRTcO
# python awis.py -u remiljw@gmail.com --key=Q3rj7tG54k7EWUjZKt3Yg5lcso1jobNw7ALYRTcO --action=urlInfo --options="&ResponseGroup=Rank&Url=sfgate.com"