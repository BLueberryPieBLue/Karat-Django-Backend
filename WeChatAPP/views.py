import hashlib

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


# ###############################################微信公众平台测试接口##################################################
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt   # 解决跨域问题
def weixin(request):
    if request.method == "GET":
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        token = "thisistoken"
        tmpArr = [token,timestamp,nonce]
        tmpArr.sort()
        string = ''.join(tmpArr).encode('utf-8')
        string = hashlib.sha1(string).hexdigest()
        if string == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("false")

#######################################################################################################################
