from django.contrib import admin

# Register your models here.
from VoteAPP.models import Competitor, Vote
class CompetitorContactAdmin(admin.ModelAdmin):
    list_display = ('id','competitorname','vote')
class VoteContactAdmin(admin.ModelAdmin):
    list_display = ('id','userid','competitorid','time')
admin.site.register(Competitor,CompetitorContactAdmin)
admin.site.register(Vote,VoteContactAdmin)