from django.contrib import admin

# Register your models here.
from UserAPP.models import *


class UserContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'Email', 'verficationCode', 'time1', 'time2', 'registState', 'errortimes', 'registtime','isroot')
class UserLogContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid', 'time', 'ip', 'ipcity','href')
class TourLogContactAdmin(admin.ModelAdmin):
    list_display = ('id','time','ip', 'ipcity','href')
class CookieContactAdmin(admin.ModelAdmin):
    list_display = ('id','usrid','cid','time1', 'time2')
admin.site.register(User,UserContactAdmin)
admin.site.register(UserLog,UserLogContactAdmin)
admin.site.register(TourLog,TourLogContactAdmin)
admin.site.register(Cookie, CookieContactAdmin)