"""caliper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from login import views as login_views
from task import views as task_views
from compare import views as compare_views
from trend import views as trend_views

urlpatterns = [
    url(r'^$',login_views.main,name='main'),
    url(r'^createuser$',login_views.userIntoCaliperDB,name='createuser'),
    url(r'^login$',login_views.login,name='login'),
    url(r'^login_verify$', login_views.login_verify, name='login_verify'),
    url(r'^downloadfile$', login_views.file_Download, name='downloadfile'),

    url(r'^task$',task_views.home,name='home'),
    url(r'^compare$',compare_views.compare,name='compare'),
    url(r'^compare/(\w+)/$',compare_views.test_aspect,name='test_aspect'),
    url(r'^trend$',trend_views.trend,name='trend'),

    url(r'^admin/', admin.site.urls),
    url(r'static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}, name='static'),
]
