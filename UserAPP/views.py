import json
import re
import time

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password

from Karat.settings import RequestHost
from UserAPP.models import User, UserLog, TourLog, Cookie
import datetime
from datetime import timedelta


# Create your views here
#######################################################################################################################################
#ASE加密
import base64
from Crypto.Cipher import AES

def pkcs7padding(text):
    bs = AES.block_size  # 16
    length = len(text)
    bytes_length = len(bytes(text, encoding='utf-8'))
    padding_size = length if(bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    padding_text = chr(padding) * padding
    return text + padding_text
def pkcs7unpadding(text):
    length = len(text)
    unpadding = ord(text[length-1])
    return text[0:length-unpadding]
def encrypt(key, content):
    key_bytes = bytes(key, encoding='utf-8')
    iv = key_bytes
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    content_padding = pkcs7padding(content)
    encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
    result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
    return result

def decrypt(key, content):
    key_bytes = bytes(key, encoding='utf-8')
    iv = key_bytes
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    encrypt_bytes = base64.b64decode(content)
    decrypt_bytes = cipher.decrypt(encrypt_bytes)
    result = str(decrypt_bytes, encoding='utf-8')
    result = pkcs7unpadding(result)
    return result
#秘钥必须16位
aes_key = 'sDf*^69Lpf!w3460'
# # 加密
# source_en = '1111111111111111'
# encrypt_en = encrypt(aes_key, source_en)
# print(encrypt_en)
# # 解密
# decrypt_en = decrypt(aes_key, encrypt_en)
# print(decrypt_en)
# print(source_en == decrypt_en)
def EncodeASE(request):
    try:
        source_en = str(request.POST.get("so"))
        encrypt_en = encrypt(aes_key, source_en)
        response = HttpResponse(json.dumps({"code": "1","en":encrypt_en}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def DecodeASE(request):
    try:
        encrypt_en=str(request.POST.get("so"))
        decrypt_en = decrypt(aes_key, encrypt_en)
        response = HttpResponse(json.dumps({"code": "1","de":decrypt_en}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
#####################################################################################################################################

# ****************************************************密码格式检查函数定义***********************************************OK
# 判断长度是否合法
def checkpwdlen(pwd):
    if len(pwd) >= 8 and len(pwd) <= 32:
        return True
    else:
        return False


def checkusrlen(usr):
    if len(usr) >= 5 and len(usr) <= 20:
        return True
    else:
        return False


# 判断是否包含大写字母
def checkContainUpper(pwd):
    pattern = re.compile('[A-Z]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


# 判断是否包含数字
def checkContainNum(pwd):
    pattern = re.compile('[0-9]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


# 判断是否包含小写字母
def checkContainLower(pwd):
    pattern = re.compile('[a-z]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


# 判断是否包含符号
def checkSymbol(pwd):
    pattern = re.compile('([^a-z0-9A-Z])+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False

# 判断是否以字母开头
def checkTop(usr):
    pattern = re.compile('(^[a-zA-Z])')
    match = pattern.findall(usr)
    if match:
        return True
    else:
        return False


# 检查密码是否合法
def checkPassword(pwd):
    # 判断密码长度是否合法
    lenOK = checkpwdlen(pwd)
    # 判断是否包含大写字母
    upperOK = checkContainUpper(pwd)
    # 判断是否包含小写字母
    lowerOK = checkContainLower(pwd)
    # 判断是否包含数字
    numOK = checkContainNum(pwd)
    # 判断是否包含符号
    symbolOK = checkSymbol(pwd)
    return (lenOK and upperOK and lowerOK and numOK and symbolOK)


# **************************************************密码格式检查函数定义************************************************OK


# *************************************************用户名nickname格式筛查***********************************************OK
# 检查用户名是否合法
def checkUsername(usr):
    # 判断用户名长度是否合法
    lenOK = checkusrlen(usr)
    topOK=checkTop(usr)
    if lenOK and topOK:
        return True
    else:
        return False


# ************************************************用户名nickname格式筛查************************************************OK


# **********************************************************************************************************************


# ************************************************邮箱格式筛查函数定义**************************************************OK
# 检查邮箱格式是否合法
def checkEmailOK(E):
    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net,org]{1,3}$', E):
        return True
    else:
        return False


# 过滤邮箱
def checkEmailBlack(E):
    Blacklist = ['bccto', 'dawin', 'chaichuang', 'jpgames', '3202', 'sltmail', '4057', 'vedmail', 'wca', 'juyouxi',
                 'oiizz', 'cr219', 'a7996', 'jnpayy', '819110', 'libivan', 'yidaiyiluwang', 'jiaxin8736',
                 'mailfavorite', 'disbox']
    for i in Blacklist:
        if not re.match('^((?!' + i + '\.).)*$', E):
            return False
    return True


# 检查邮箱（格式、域名）是否合法
def checkEmail(E):
    if checkEmailOK(E)and checkEmailBlack(E):
        return True
    else:
        return False


# **********************************************邮箱格式筛查函数定义****************************************************OK

# **********************************************************************************************************************

# ******************************************************用户名验证********************************************************OK
def CheckUsername(request):
    ####请求方式：POST
    ####获取参数：nickname
    ####code返回值：
    # 请求失败：0；用户名允许注册：1；用户名已经注册：2；用户名不合法：3；
    try:
        # 用户名
        username = str(request.POST.get("username"))
        # 验证用户名是否合法
        if not checkUsername(username):
            response = HttpResponse(json.dumps({"code": "3"}))
        else:
            # 验证用户名是否已经注册
            try:
                # 用户名已被注册
                usr = User.objects.get(username=username)
                response = HttpResponse(json.dumps({"code": "2"}))
            except Exception as e:
                #print(e)
                response = HttpResponse(json.dumps({"code": "1"}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response



# **********************************************************************************************************************

# **************************************************登录密码检查********************************************************OK
def CheckPassword(request):
    ####请求方式：POST
    ####获取参数：password
    ####code返回值：
    # 请求失败：0；
    # 密码合法：1；
    # 密码不合法：2；
    try:
        # 获取密码
        password = str(request.POST.get("password"))
        if checkPassword(password):
            response = HttpResponse(json.dumps({"code": "1"}))
        else:
            response = HttpResponse(json.dumps({"code": "2"}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


# **************************************************登录密码验证********************************************************OK

# **********************************************************************************************************************

# ***************************************************邮箱审查***********************************************************OK
def CheckEmail(request):
    ####请求方式：POST
    ####获取参数：Email
    ####code返回值：
    # 请求失败：0；邮箱合法：1；邮箱已经注册：2；邮箱不合法：3；
    try:
        # 收件邮箱
        Email = str(request.POST.get("Email"))
        # 验证邮箱是否合法
        if not checkEmail(Email):
            response = HttpResponse(json.dumps({"code": "3"}))#邮箱不合法 不允许注册  不允许登录 不允许resetpwd
        else:
            # 验证邮箱是否已经注册
            try:
                usr = User.objects.get(Email=Email)
                if usr.registState=="1":
                    response = HttpResponse(json.dumps({"code": "2"}))# 邮箱已被注册 不允许注册 允许登录 允许resetpwd
                else:
                    response = HttpResponse(json.dumps({"code": "4"}))# 邮箱未激活 允许注册 不允许登录 不允许resetpwd
            except Exception as e:
                # print(e)
                response = HttpResponse(json.dumps({"code": "1"}))# 邮箱未注册 允许注册 不允许登录 不允许resetpwd
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))#SYSTEM ERROR
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


# ************************************************邮箱审查**************************************************************OK

# **********************************************************************************************************************

# ***********************************************游客注册***************************************************************OK

def Register(request):
    try:
        ####请求方式：POST
        ####获取参数：Email;token;username;password;
        ####code返回值：
        # 请求失败：0；注册成功：1；验证码错误：2；验证码失效：3；
        token = str(request.POST.get("token"))
        Email = str(request.POST.get("Email"))
        username=str(request.POST.get("username")).strip() #去掉字符串首尾指定字符（默认为空格或换行符）
        password = str(request.POST.get("password"))
        if checkUsername(username)and checkPassword(str(request.POST.get("password")))and checkEmail(Email):
            per = User.objects.get(Email=Email)
            time1=float(per.time1)
            time2 = float(per.time2)
            verficationCode=per.verficationCode
            # time3 介于Tim1与time2之间  开始验证验证码 反之验证码失效重新发送邮件
            # 时间
            import time
            time3 = time.time()  # 当前秒数时间戳
            ## 验证码有效
            if time3>time1 and time3<time2:
                # 验证码正确
                if token.strip()==verficationCode.strip():
                    if per.registState=="0":
                        #更改registState=1即注册成功
                        per.registState=1
                        # 密码##########通过django自带的类库，来加密用户密码，同一明文每次生成的密文不同
                        per.password=make_password(password)
                        per.username=username
                        import time
                        timeArray = time.localtime(time3)
                        Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        per.registtime=Time
                        per.save()
                        response = HttpResponse(json.dumps({"code": "1"}))
                else:
                    response = HttpResponse(json.dumps({"code": "2"}))
            else:
                response = HttpResponse(json.dumps({"code": "3"}))
        else:
            response = HttpResponse(json.dumps({"code": "0"})) #验证失败
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


# **********************************************游客注册****************************************************************OK

# **********************************************************************************************************************

# *************************************************游客登录*************************************************************OK
def Loginer(request):  # 登录
    ####请求方式：POST
    ####获取参数：Email；password；
    ####code返回值：
    # 请求失败：0；登录成功：1；邮箱未注册：2；密码错误：3；
    try:
        # 收件邮箱
        Email = str(request.POST.get("Email"))
        # 获取密码
        password = request.POST.get("password")
        #print(request.POST)
        try:
            per = User.objects.get(Email=Email)
            pwd = per.password
            if per.registState=="1":
                #print(check_password(str(password),str(pwd)))
                #print(password)
                #print(pwd)
                if check_password(password.strip(),pwd.strip()):
                    per.errortimes=0
                    per.save()
                   # session
                    request.session['username'] = per.username
                    request.session['id'] = per.id
                    request.session['Email'] = per.Email
                    response = HttpResponse(json.dumps({"code": "1", "id": per.id}))  # 登录成功
                    # cookie
                    # now = datetime.datetime.utcnow()
                    # delta = timedelta(seconds=500)
                    # value = now + delta
                    # response.set_cookie("id", per.id, expires=value, path='/', domain=None, secure=False,httponly=True)
                else:
                    per.errortimes=int(per.errortimes)+1
                    if per.errortimes >= 6:
                        per.registState = 0
                    per.save()
                    response = HttpResponse(json.dumps({"code": "3","errortimes":per.errortimes,"registState":per.registState}))
            elif per.registState=="0":
                response = HttpResponse(json.dumps({"code": "4"}))#账号异常已冻结
        except Exception as e:
            print(e)
            response = HttpResponse(json.dumps({"code": "2"}))#邮箱未注册
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


#******************************************************游客登录********************************************************OK

#************************************************************************************************************************

# *****************************************************密码重置********************************************************OK

def Resetpwd(request):  # 密码重置
    try:
        ####请求方式：POST
        ####获取参数：Email;token;password;
        ####code返回值：
        # 请求失败：0；注册成功：1；验证码错误：2；验证码失效：3；
        token = str(request.POST.get("token"))
        Email = str(request.POST.get("Email"))
        password = str(request.POST.get("password"))
        # print(request.POST)
        # print(password)
        if checkPassword(str(request.POST.get("password"))) and checkEmail(Email):
            per = User.objects.get(Email=Email)
            time1 = float(per.time1)
            time2 = float(per.time2)
            verficationCode = per.verficationCode
            # time3 介于Tim1与time2之间  开始验证验证码 反之验证码失效重新发送邮件
            # 时间
            import time
            time3 = time.time()  # 当前秒数时间戳
            ## 验证码有效
            if time3 > time1 and time3 < time2:
                # 验证码正确
                if token.strip() == verficationCode.strip():
                    if per.id==0:
                        response = HttpResponse(status=404)
                    else:
                        if (per.registState == "0")|(per.registState == "1"):
                            # 更改registState=1
                            per.registState = 1
                            # 密码##########通过django自带的类库，来加密用户密码，同一明文每次生成的密文不同
                            per.password = make_password(password)
                            per.save()
                            response = HttpResponse(json.dumps({"code": "1"}))
                        else:
                            response = HttpResponse(json.dumps({"code": "4"}))#账号异常
                else:
                    response = HttpResponse(json.dumps({"code": "2"}))
            else:
                response = HttpResponse(json.dumps({"code": "3"}))
        else:
            response = HttpResponse(json.dumps({"code": "0","info":"ERROR"}))  # 验证失败
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


# *****************************************************密码重置********************************************************OK

# **********************************************************************************************************************

# *****************************************************响应页面*******************************************************OK
def Regispage(request):  #########返回注册页
    title = {
        'head': '注册',
        'title': "欢迎使用山东理工大学新闻网注册系统",
        'buttontitle': '注册',
        'login': 0,
        'regis': 1,
        'reset': 0
    }
    return render(request, 'Entry.html', {'title': title,"RequestHost":RequestHost})


def Loginpage(request):  ############返回登录页
    title = {
        'head': '登录',
        'title': "欢迎使用山东理工大学新闻网登录系统",
        'buttontitle': '登录',
        'login': 1,
        'regis': 0,
        'reset': 0
    }
    return render(request, 'Entry.html', {'title': title,"RequestHost":RequestHost})


def Resetpwdpage(request):  ############返回重置密码页
    title = {
        'head':'重置密码',
        'title': "密码重置",
        'buttontitle': '重置',
        'login': 0,
        'regis': 0,
        'reset': 1
    }
    return render(request, 'Entry.html',  {'title': title,"RequestHost":RequestHost})
# *****************************************************响应页面**********************************************************

# ***********************************************************************************************************************

# ***********************************************************************************************************************
#注销
def Logouter(request):
    try:
        del request.session["username"]
        del request.session["id"]
        del request.session["Email"]
        response = HttpResponse(json.dumps({"code": "1"}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

#检查用户登录
def CheckLogin(request):
    #0 请求失败
    #1 用户已登录
    # 2:用户未登录
    try:
        # id=request.session.get("id")
        # username = request.session.get("username")
        # Email=request.session.get("Email")
        id = request.POST.get("id")
        #print("id**"+id)
        if id==None:
            response = HttpResponse(json.dumps({"code": "2"}))
        else:
            per = User.objects.get(id=id)
            request.session['username'] = per.username
            request.session['id'] = per.id
            print("perid："+str(per.id))
            request.session['Email'] = per.Email
            response = HttpResponse(json.dumps({"code": "1"}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def GetIP(request):
    try:
        ip = request.POST.get("ip")
        ipcity = request.POST.get("ipcity")
        href = request.POST.get("href")
        id=request.session.get("id")
        timeArray = time.localtime(time.time())
        Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        if id==None:
            tlog = TourLog()
            tlog.ip = ip
            tlog.ipcity = ipcity
            tlog.time = Time
            tlog.href = href
            tlog.save()
            response = HttpResponse(json.dumps({"code": "2"}))
        else:
            ulog=UserLog()
            ulog.userid=id
            ulog.ip=ip
            ulog.ipcity=ipcity
            ulog.time=Time
            ulog.href=href
            ulog.save()
            response = HttpResponse(json.dumps({"code": "1"}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def SetCookie(request):
    try:
        params=str(request.POST.get("params"))
        uid=decrypt(aes_key, params)
        import random
        seed = "012456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sa = []
        for i in range(25):
            sa.append(random.choice(seed))
        cookieid = "".join(sa)
        time1 = time.time()
        time2 = (time.time() + 604800)
        try:
            per = User.objects.get(id=uid)
            cookie=Cookie.objects.get(usrid=uid)
            cookie.usrid = uid
            cookie.cid = cookieid
            cookie.time1 = time1
            cookie.time2 = time2
            cookie.save()
        except:
            cookie = Cookie()
            cookie.usrid=uid
            cookie.cid = cookieid
            cookie.time1 = time1
            cookie.time2 = time2
            cookie.save()
        response = HttpResponse(json.dumps({"code": "1",'cookieid':cookieid}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def GetCookie(request):
    try:
        cid = str(request.POST.get("cid"))
        cookie=Cookie.objects.get(cid=cid)
        uid=cookie.usrid
        usr=User.objects.get(id=uid)
        umane=usr.username
        time1 =float(cookie.time1)
        time2=float(cookie.time2)
        time3=time.time()
        if time3>=time1 and time3<=time2:
            response = HttpResponse(json.dumps({"code": "1","umane":umane}))
        else:
            response = HttpResponse(json.dumps({"code": "0"}))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"code": "0"}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response