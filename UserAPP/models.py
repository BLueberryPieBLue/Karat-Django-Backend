from django.db import models

# Create your models here.

#表userapp_user
class User(models.Model):
    #Django会自动创建主键id
    username=models.CharField(max_length=255)#用户名Nickname
    password=models.CharField(max_length=255)#加密后的用户密码密文 #########在数据库中存储加密后的密码而非明文#######
    Email=models.CharField(max_length=255)#用户邮箱
    verficationCode=models.CharField(max_length=255)#邮箱验证码
    time1=models.CharField(max_length=255)#发送邮件时间
    time2 = models.CharField(max_length=255)#发送邮件时间+30min即验证码有效期
    registState = models.CharField(max_length=255)#注册状态 默认为0 激活用户为1 锁定用户为0
    errortimes = models.CharField(max_length=255)#密码输入错误次数 错误第6次即锁定用户
    registtime = models.CharField(max_length=255)#注册时间
    isroot=models.CharField(max_length=255)

#cookie
class Cookie(models.Model):
    usrid = models.CharField(max_length=255)
    cid = models.CharField(max_length=255)
    time1 = models.CharField(max_length=255)
    time2 = models.CharField(max_length=255)

#用户浏览日志
class UserLog(models.Model):
    userid=models.CharField(max_length=255)
    time=models.CharField(max_length=255)
    ip=models.CharField(max_length=255)
    ipcity=models.CharField(max_length=255)
    href=models.CharField(max_length=255)

#游客浏览日志
class TourLog(models.Model):
    time=models.CharField(max_length=255)
    ip=models.CharField(max_length=255)
    ipcity=models.CharField(max_length=255)
    href=models.CharField(max_length=255)