from django.contrib import admin


from KaratAPP.models import Vote

# Register your models here.
#投票测试admin
class VoteContactAdmin(admin.ModelAdmin):
    list_display = ('id','data')
admin.site.register(Vote,VoteContactAdmin)
###################################################################