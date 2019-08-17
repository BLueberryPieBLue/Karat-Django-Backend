"""Karat URL Configuration

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
from django.urls import include
from RootAPP import views as RootAPPviews

urlpatterns = [
    ######################################################################################
    #Admin
    url(r'^Admin/', admin.site.urls),
    url(r'^Admin/webshell/', include('webshell.urls')),
    ######################################################################################
    # Root
    url(r"^LoginRoot/", RootAPPviews.LoginRoot),
    url(r"^LogoutRoot/", RootAPPviews.LogoutRoot),
    url(r"^Code/", RootAPPviews.Code),
    url(r"^Prt/", RootAPPviews.Prt),
    url(r"^Del/", RootAPPviews.Del),
    url(r"^CMD/", RootAPPviews.CMD),
    url(r'^FTP/(?P<url>.+)', RootAPPviews.FTP),
    url(r"^FTPDownload/(?P<url>.+)", RootAPPviews.FTPDownload),
    url(r"^FTPDir/(?P<url>.+)", RootAPPviews.FTPDownloadDir),
    url(r"^Upload/(?P<url>.+)", RootAPPviews.Upload),
    ######################################################################################

]
