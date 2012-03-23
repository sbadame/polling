from polls.models import Public_Poll,Private_Poll,Choice,Vote
from django.contrib import admin

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class VoteInline(admin.TabularInline):
    model = Vote
    extra = 1

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Total Votes', {'fields': ['total_votes']}),
        ('Date Created Info', {'fields': ['date_created']}),
        ('Date Expire Info', {'fields': ['date_expire']}),
    ]
    inlines = [ChoiceInline,VoteInline]
    list_display = ('question', 'get_absolute_url', 'get_vote_url', 'total_votes', 'date_created', 'date_expire')
    list_filter = ['date_created']
    search_fields = ['question']



admin.site.register(Public_Poll, PollAdmin)
admin.site.register(Private_Poll, PollAdmin)
