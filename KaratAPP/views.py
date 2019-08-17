import os
from django.http import HttpResponse
from django.shortcuts import render
import json
# Create your views here.
from Karat.settings import RequestHost
from VoteAPP.models import Vote
from UserAPP.models import User
import logging
logger=logging.getLogger("console")

###########################################################欢迎页面#####################################################################
def hello(request):
    IP(request)
    return render(request,"team.htm",{"RequestHost":RequestHost})

###########################################################投票测试###################################################################
#返回票数
def getvote(request):
    print("getvoter")
    try:
        vote=Vote.objects.get(id=0)
        response = HttpResponse(json.dumps({'code':"1","vote": vote.data}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({'code': "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
#写入
def setvote(request):
    print(request.POST)
    customname=str(request.POST.get("username")).strip()
    print("voternaem"+customname)
    custom=User.objects.get(username=customname)
    if not custom:
        print("no custom vote record")

    try:
        vote = Vote.objects.get(id=0)
        vote2=Vote()
        vote2.data=str(int(vote.data)+1)
        Vote.objects.filter(id=0).update(data=vote2.data)
        response = HttpResponse(json.dumps({'code': "1","vote":vote2.data}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({'code': "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

#投票页面
def vote(request):
    return render(request, "vote.html",{"RequestHost":RequestHost})
####################################################################################################################
def cookie(request):
    return render(request, "cookie.html",{"RequestHost":RequestHost})
######################################################################################################################
def IP(request):
    try:
        import time
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        outfile = open(os.path.join(BASE_DIR, "./log.txt"), 'a+', encoding='UTF-8')
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        print(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())),ip,file=outfile)
    except Exception as e:
        print(e)
