from polls.models import Poll,Choice,Vote
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
        ('Date Created Info', {'fields': ['date_created']}),
        ('Date Expire Info', {'fields': ['date_expire']}),
    ]
    inlines = [ChoiceInline,VoteInline]
    list_display = ('question', 'date_created', date_expire)
    list_filter = ['date_created']
    search_fields = ['question']

admin.site.register(Poll, PollAdmin)
