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
from django.views.static import serve

from Karat.settings import MEDIA_ROOT, SCRIPT_ROOT
from KaratAPP import views as KaratAPPviews
from WeChatAPP import views as WeChatAPPviews
from VoteAPP import views as VoteAPPviews
from EmailAPP import views as EmailAPPviews
from UserAPP import views as UserAPPviews


urlpatterns = [
    ######################################################################################
    # Root Dangerous document path
    url(r"^KaratRoot/",include('RootAPP.urls')),
    ######################################################################################
    # 可引用文件路径
    # 视频图片文件
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),
    # 脚本文件
    url(r'^script/(?P<path>.*)/$', serve, {"document_root": SCRIPT_ROOT}),
    ######################################################################################
    # 欢迎页面
    url(r"^$", KaratAPPviews.hello),
    # cookie 测试
    url(r"^cookie", KaratAPPviews.cookie),
    ######################################################################################
    # 投票测试
    url(r"^SetVote/",VoteAPPviews.SetVote),
    url(r"^GetVote/", VoteAPPviews.GetVote),
    # url(r"^vote/", KaratAPPviews.vote),
    ######################################################################################
    # 微信公众平台测试接口
    url(r"^wx/", WeChatAPPviews.weixin),
    ######################################################################################
    # 全景地图
    url(r"^Map/",include('MapAPP.urls')),
    ######################################################################################
    # 邮件
    # SendEmail（注册验证、重置）
    url(r"^SendEmail/", EmailAPPviews.SendEmail),
    #***********************************************************************************
    # 注册
    url(r"^Regispage/", UserAPPviews.Regispage),
    url(r"^Register/", UserAPPviews.Register),
    # 登录
    url(r"^Loginpage/", UserAPPviews.Loginpage),
    url(r"^Loginer/", UserAPPviews.Loginer),
    # 注销
    url(r"^Logouter/", UserAPPviews.Logouter),
    # 密码重置
    url(r"^Resetpwdpage/", UserAPPviews.Resetpwdpage),
    url(r"^Resetpwd/", UserAPPviews.Resetpwd),
    # 检查用户名
    url(r"^CheckUsername/", UserAPPviews.CheckUsername),
    # 检查密码
    url(r"^CheckPassword/", UserAPPviews.CheckPassword),
    # 检查用户邮箱
    url(r"^CheckEmail/", UserAPPviews.CheckEmail),
    # 检查用户登录
    url(r"^CheckLogin/", UserAPPviews.CheckLogin),
    # GET IP
    url(r"^GetIP/", UserAPPviews.GetIP),
    # set cookie
    url(r"^SetCookie/", UserAPPviews.SetCookie),
    # get cookie
    url(r"^GetCookie/", UserAPPviews.GetCookie),
    # *************************************************************************************
    # #ASE加密 解密
    url(r"^En/", UserAPPviews.EncodeASE),
    url(r"^De/", UserAPPviews.DecodeASE),
    # **************************************投票******************************************
    # 更新选手
    url(r"^EqualAdjust/", VoteAPPviews.EqualAdjust),
    # 用户投票
    url(r"^SetVote/", VoteAPPviews.SetVote),
    # 返回选手票数
    url(r"^GetVote/", VoteAPPviews.GetVote),
    # 返回当前登录用户下选手是否被投票
    url(r"^VoteAdjust/", VoteAPPviews.VoteAdjust),
    # *****投票页测试一会儿删除***********
    url(r"^Votepage/", VoteAPPviews.Votepage),
    # *****投票页测试一会儿删除***********
    # **************************************************************************************
    # ##################################################################################################################################
]
