"""PageTester URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from landingPageTester import views as LPT_views

urlpatterns = [
	path('admin/', admin.site.urls),
	# path('', LPT_views.index, name='index'),
	# path('test/', LPT_views.webinfo, name='topsites'),
	# path('landingpagetester/', LPT_views.TestPage, name='testPage')
	path('add_page/', LPT_views.webinfo, name='addpage'),
	path('get_status/', LPT_views.get_status, name='status'),
	path('delete_url/<str:pk>',LPT_views.delete_url, name='delete_url'),
	path('get_page_signups/', LPT_views.get_page_signups, name='get_page_signups'),
]
