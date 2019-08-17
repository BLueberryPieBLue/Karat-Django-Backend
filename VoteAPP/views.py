import json

from django.http import HttpResponse
from django.shortcuts import render

from UserAPP.models import User,UserLog
from VoteAPP.models import Competitor, Vote #选手表、用户投票记录表


# Create your views here.


########################################################################################################################
def EqualAdjust(request):
    ####请求方式：POST
    ####获取参数：comp；
    ####code返回值：
    #请求失败：0；选手更新成功：1；
    try:
        #最新选手列表
        comp=request.POST.get("comp").split("#")
        username = request.session.get("username")
        for i in comp:
            if  i!="" and i !=" " and i!="  " and i!="   ":
                # i=i.split(" ").join()
                #print(i)
                try:
                    Comp=Competitor.objects.get(competitorname=i)
                except:
                    # 保存数据库中没有的选手
                    Comp = Competitor()
                    Comp.competitorname=i
                    Comp.vote =0
                    Comp.save()
                    print("ok")
        response = HttpResponse(json.dumps({"code":"1","username":username}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code":"0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

############################################################################################################################
def SetVote(request):
    ####请求方式：POST
    ####获取参数：competitorname ;
    ####code返回值：
    #请求失败：0；
    # 用户投票成功：1；
    # 今天已经投完5票再次投票：2 ；
    # 用户未登录的情况下请求投票-1;

    try:
        # 选手名字
        compAnduser=str(request.POST.get("compAnduser")).split("@")
        competitorname=compAnduser[0]
        userid =compAnduser[1]
        print( competitorname)
        #print(userid)
        if userid == None or userid=='undefined':
            response=HttpResponse(json.dumps({"code":'-1'}))
        else:
            #投票时间
            import time
            time = time.time()  # 时间戳
            comp=Competitor.objects.get(competitorname=competitorname)
            competitorid=comp.id
            vote=Vote()
            vote.userid=userid
            vote.competitorid = competitorid
            vote.time = time
            # 选手票数+1
            comp.vote=int(comp.vote)+1
            #print(comp.vote)
            #判断每人每天投5票---》是否
            import time
            t = time.localtime(time.time())
            #time1当日00:00:00
            time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))
            # time2当日23:59:59
            time2 = time1 + 24 * 60 * 60 - 1
            votea = Vote.objects.filter(userid=userid)
            j = 0
            for i in votea:
                #print(i.time)
                if float(i.time) >= time1 and float(i.time) <= time2:
                    j = j + 1
            #print(j)
            if j< 5:#每人每天最大投票数
                #保存
                vote.save()
                comp.save()
                response = HttpResponse(json.dumps({"code":"1"}))#投票成功
            else:
                response = HttpResponse(json.dumps({"code": "2"}))  # 今天已经投完5票再次投票
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code":"0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


############################################################################################################################
def GetVote(request):
    ####请求方式：POST
    ####code返回值：
    #请求失败：0；查询成功：1；
    ####votenum返回值是一个json列表，{"选手名":"票数",选手名":"票数"} ************前端****Unicode编码js转中文***********
    try:
        #从数据库查询票数
        obj = Competitor.objects.all().values()
        s = "{"
        j=0
        for i in obj:
            s+='"'+i.get('competitorname')+'"'+":"+'"'+i.get('vote')+'"'
            j=j+1
            if j!=len(obj):
                s+=','
        s += "}"
        s=json.loads(s)
        #print(s)
        response = HttpResponse(json.dumps({"code":"1","s":s}))#json列表，{"选手名":"票数",选手名":"票数"} ************前端****Unicode编码js转中文***********
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code":"0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

############################################################################################################################
def VoteAdjust(request):
    ####请求方式：POST
    ####code返回值：
    #请求失败：0；查询成功：1；
    ####voteadjust返回值：这是一个json列表 当日该用户投票给谁
    try:
        userid = request.session.get("id")
        import time
        t = time.localtime(time.time())
        time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))
        time2=time1+24*60*60-1
        #从数据库查询票数
        vote=Vote.objects.filter(userid= userid)
        comps=[]
        Comps=[]
        for i in vote:
            #print(i.time)
            if float(i.time)>=time1 and float(i.time) <=time2:
                #print(i.competitorid)
                comps.append(i.competitorid)
        for i in comps:
            com=Competitor.objects.get(id=i)
            Comps.append(com.competitorname)
        #print(Comps)
        s = ""
        for i in Comps:
            s +=i+ ' '
        #print(s)
        response = HttpResponse(json.dumps({"code":"1","s":s}))#当日该用户投票给谁(返回unicode编码 空格分割)
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code":"0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
#########################################################################################################################
def Votepage(request):  #########返回投票页//测试，一会儿删除，
    return render(request, 'listcolumn.htm')

