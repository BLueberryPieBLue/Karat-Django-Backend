from django.db import models

# Create your models here.
##########################################################################
#投票
class Vote(models.Model):
    data=models.CharField(max_length=255)

##########################################################################