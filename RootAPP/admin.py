from django.contrib import admin
from django.utils.translation import gettext_lazy

# Register your models here.
admin.site.site_header =gettext_lazy( 'Karat administration')
admin.site.site_title = gettext_lazy( 'Karat site admin')
admin.site.index_title =gettext_lazy( 'Site administration')
from django.contrib.admin.models import *
class AdminContactAdmin(admin.ModelAdmin):
    list_display = ('id','action_time','user','content_type','object_id','object_repr','action_flag','change_message')
admin.site.register(LogEntry,AdminContactAdmin)

