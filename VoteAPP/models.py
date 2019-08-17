from django.db import models

# Create your models here.

#表voteapp_user
class Competitor(models.Model):
    #y选手信息表
    # 这里会自动创建主键id
    competitorname=models.CharField(max_length=255)#选手名
    vote=models.CharField(max_length=255)#票数

#表voteapp_vote
class Vote(models.Model):
    #游客投票信息表
    # 这里会自动创建主键id
    userid=models.CharField(max_length=255)#投票者id
    competitorid = models.CharField(max_length=255)#被投票者id
    time=models.CharField(max_length=255)#投票时间
