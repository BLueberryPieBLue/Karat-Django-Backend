import json
import re

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from UserAPP.models import User
############################################################################################################################
def SendEmail(request):
    # 前端验证发邮件的前提：用户名和密码符合规则
    ####请求方式：POST
    ####获取参数：Email；task；
    ####code返回值：
    #请求失败：0；邮件发送成功：1；
    ####info返回值：详细信息

    #POST
    #收件邮箱
    receverEmail=str(request.POST.get("Email"))
    #任务
    task = str(request.POST.get("task"))
    if task == '0':
        taskname = "用户注册"
    if task == '1':
        taskname = "重置密码"

    #验证码 这里区分大小写
    import random
    seed="012456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa=[]
    for i in range(12):
        sa.append(random.choice(seed))
    verficationCode="".join(sa)

    #时间
    import time
    # print(time.time())
    # print(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))
    # print(time.time() + 1800)
    # print(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time() + 1800)))
    time1 = time.time() #当前秒数时间戳
    time2 = (time.time() + 1800) #30分钟之后
    if task == '0':#注册
        #邮箱未激活 数据库中含有邮箱
        try:
            user = User.objects.get(Email=receverEmail)
            if user.registState == "0":
                user.verficationCode = verficationCode
                user.time1 = time1
                user.time2 = time2
                user.registState = 0
                user.errortimes = 0
                # 保存
                user.save()
        except Exception as e:
            # print(e)
            # 邮箱未注册 数据库中不含有邮箱
            #存入数据库信息
            user=User()
            user.Email=receverEmail
            user.verficationCode=verficationCode
            user.time1=time1
            user.time2=time2
            user.registState=0
            user.errortimes=0
            # 保存
            user.save()
    if task == '1': # 重置密码
        # 邮箱未激活 数据库中含有邮箱
        try:
            user = User.objects.get(Email=receverEmail)
            if (user.registState == "1")|(user.registState == "0"):
                if user.id == 0:
                    return HttpResponse(status=404)
                else:
                    user.verficationCode = verficationCode
                    user.time1 = time1
                    user.time2 = time2
                    user.registState = 0
                    user.errortimes = 0
                    # 保存
                    user.save()
        except Exception as e:
            # print(e)
            # 邮箱未注册 数据库中不含有邮箱
            response = HttpResponse(json.dumps({"code": "0"}))
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response

    ###################################################################
    import smtplib
    from email import encoders
    from email.mime.base import MIMEBase
    from email.header import Header
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText  # 引入smtplib和MIMETex
    port = 465    # port = 25
    senderSmtp = 'smtp.163.com'  # 发件人的SMTP服务器
    senderEmail = '17853314162@163.com'  # 发件人邮箱
    tokenPwd = 'ClL194210310801'  # 发件人邮箱的口令
    #receverEmail = '17853314162@163.com'  # 测试收件邮箱
    mail_extra_image_url = r'D:\KARAT\Data\img\Karat.jpg'
    mailSubject = "Karat邮箱验证-"+taskname
    mailContent ="""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title></title>
        <link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">  
        <script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
        <script src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <meta charset="utf-8" />
    </head>
    <body>
        <div class="qmbox qm_con_body_content qqmail_webmail_only" id="mailContentContainer" style="">
            <style type="text/css">
                .qmbox body {
                    margin: 0;
                    padding: 0;
                    background: #fff;
                    font-family: "Verdana, Arial, Helvetica, sans-serif";
                    font-size: 14px;
                    line-height: 24px;
                }
                .qmbox div, .qmbox p, .qmbox span, .qmbox img {
                    margin: 0;
                    padding: 0;
                }
                .qmbox img {
                    border: none;
                }
                .qmbox .contaner {
                    margin: 0 auto;
                }
                .qmbox .title {
                    margin: 0 auto;
                    background: url() #CCC repeat-x;
                    height: 30px;
                    text-align: center;
                    font-weight: bold;
                    padding-top: 12px;
                    font-size: 16px;
                }
                .qmbox .content {
                    margin: 4px;
                }
                .qmbox .biaoti {
                    padding: 6px;
                    color: #000;
                }
                .qmbox .xtop, .qmbox .xbottom {
                    display: block;
                    font-size: 1px;
                }
                .qmbox .xb1, .qmbox .xb2, .qmbox .xb3, .qmbox .xb4 {
                    display: block;
                    overflow: hidden;
                }
                .qmbox .xb1, .qmbox .xb2, .qmbox .xb3 {
                    height: 1px;
                }
                .qmbox .xb2, .qmbox .xb3, .qmbox .xb4 {
                    border-left: 1px solid #BCBCBC;
                    border-right: 1px solid #BCBCBC;
                }
                .qmbox .xb1 {
                    margin: 0 5px;
                    background: #BCBCBC;
                }
                .qmbox .xb2 {
                    margin: 0 3px;
                    border-width: 0 2px;
                }
                .qmbox .xb3 {
                    margin: 0 2px;
                }
                .qmbox .xb4 {
                    height: 2px;
                    margin: 0 1px;
                }
                .qmbox .xboxcontent {
                    display: block;
                    border: 0 solid #BCBCBC;
                    border-width: 0 1px;
                }
                .qmbox .line {
                    margin-top: 6px;
                    border-top: 1px dashed #B9B9B9;
                    padding: 4px;
                }
                .qmbox .neirong {
                    padding: 6px;
                    color: #666666;
                }
                .qmbox .foot {
                    padding: 6px;
                    color: #777;
                }
                .qmbox .font_darkblue {
                    color: #006699;
                    font-weight: bold;
                }
                .qmbox .font_lightblue {
                    color: #008BD1;
                    font-weight: bold;
                }
                .qmbox .font_gray {
                    color: #888;
                    font-size: 12px;
                }
            </style>
            <div class="contaner" >
                <div class="title well">Karat """+taskname+""" 邮箱验证</div>
                <div class="content">
                    <p class="biaoti"><b>亲爱的用户，您好！</b></p>
                    <b class="xtop"><b class="xb1"></b><b class="xb2"></b><b class="xb3"></b><b class="xb4"></b></b>
                    <div class="xboxcontent">
                        <div class="neirong">
                            <p><b>"""+taskname+"""所需的验证码：</b><span class="font_lightblue"><span id="yzm" data="$(captcha)" onclick="return false;" t="7" style="border-bottom: 1px dashed rgb(204, 204, 204); z-index: 1; position: static;">"""+verficationCode+"""</span></span><br><span class="font_gray">(请输入该验证码完成"""+taskname+"""验证，验证码区分大小写，验证码30分钟内有效！)</span></p>
                            <div class="line">如果您未申请Karat"""+taskname+"""服务，请忽略该邮件。</div>
                        </div>
                    </div>
                    <b class="xbottom"><b class="xb4"></b><b class="xb3"></b><b class="xb2"></b><b class="xb1"></b></b>
                    <p class="foot">如果仍有问题，请拨打我们的服务专线: 
                        <span  onclick="return false;" t="7" style="border-bottom: 1px dashed rgb(204, 204, 204); z-index: 1; position: static;">
                            0533-2786727
                        </span>
                        <img src="cid:0" style="width:800px;">
                    </p>
                </div>
            </div>
            <style type="text/css">
                .qmbox style, .qmbox script, .qmbox head, .qmbox link, .qmbox meta {
                    display: none !important;
                }
            </style>
        </div>
    </body>
    </html>
    """


    msg = MIMEMultipart()
    msg['subject'] = Header(mailSubject, 'utf-8').encode()  # 设置邮件标题
    msg['from'] = senderEmail  # 设置发送人
    msg['to'] = receverEmail  # 设置接收人
    msg.attach(MIMEText(mailContent, 'html', 'utf-8'))
    with open(mail_extra_image_url, 'rb') as f:
        mime = MIMEBase('image', 'jpg', filename='附件.jpg')  # 设置附件的MIME和文件名，这里是png类型:
        mime.add_header('Content-Disposition', 'attachment', filename='附件.png')  # 加上必要的头信息:
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        mime.set_payload(f.read())  # 把附件的内容读进来:
        encoders.encode_base64(mime)  # 用Base64编码:
        msg.attach(mime)

    try:
        server = smtplib.SMTP_SSL(senderSmtp, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
        server.set_debuglevel(1)
        server.login(senderEmail, tokenPwd)  # 登陆邮箱
        server.sendmail(senderEmail, [receverEmail], msg.as_string())  # 发送邮件
        server.quit()
        print('Email to:' + receverEmail + ' is successful')
        response = HttpResponse(json.dumps({"code":"1","info": 'Email to:' + receverEmail + ' is successful'}))
    except smtplib.SMTPException as err:
        print('Email to:' + receverEmail + ' is faild')
        response = HttpResponse(json.dumps({"code":"0","info": 'Email to:' + receverEmail + ' is faild'+str(err)}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
######################################################################################################################################