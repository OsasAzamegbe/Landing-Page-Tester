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
from django.urls import path, include
from landingPageTester import views as LPT_views
from django.urls import path, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
	# path('v1/', include('landingPageTester.urls')),
    path('', LPT_views.index, name='index'),
    path('add_page/', LPT_views.add_page, name='add_page'),
    path('get_status/', LPT_views.get_status, name='get_status'),
    # path('landingpagetester/', LPT_views.TestPage, name='testPage'),
    path('delete_page/<int:pk>/', LPT_views.delete_page, name='delete_page'),
    path('manage/<int:pk>/', LPT_views.manage, name='manage'),
	path('edit_url/', LPT_views.edit_url, name='edit_url'),
	path('get_url/<int:pk>/', LPT_views.get_url, name='get_url')
]
                               