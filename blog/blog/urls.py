"""blog URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from myblog import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include("ckeditor_uploader.urls")),
    url(r'^articles/([0-9]+)$', views.article),
    url(r'^$', views.index),
    url(r'^about$', views.aboutblog),
    url(r'^leavemessage$', views.leavemessage),
    url(r'^mask/(\S+)$', views.mask),
    url(r'^type/(\S+)$', views.category),
    url(r'^([0-9]+)/([0-9]+)$', views.date),
    url(r'^([0-9]+)$', views.indexPage),
    url(r'^mask/(\S+)/([0-9]+)$', views.mask),
    url(r'^type/(\S+)/([0-9]+)$', views.category),
    url(r'^([0-9]+)/([0-9]+)/([0-9]+)$', views.datePage),
]