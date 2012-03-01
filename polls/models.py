import datetime
from django.db import models

# The rundown on how to to deal with models
# =========================================
#   Help my database is out dated!!
#       1.) Go up one directory and run: "./manage.py migrate polls"
#
#   I wanna add/change/remove a field!
#       1.) Make your changes here
#       2.) Go up 1 directory and run: "./manage.py schemamigration polls --auto"
#       3.) You'll have a new file in polls/migration. Commit those to git.
#       4.) If you don't want to modify any data then just run: "./manage.py migrate polls"
#
#   But I need to change the value of some fields!
#       2.) Run "./manage.py datamigration polls <enter a super cool name here>"
#       3.) Edit the forwards() and backwards() functions in
#             polls/migration/<enter a super cool name here>.py to do what you want with the models.
#       4.) Commit polls/migration/<enter a super cool name here>.py to git
#       5.) Run "./manage.py migrate polls"

class Poll(models.Model):
    question = models.CharField(max_length=200)
    date_created = models.DateTimeField('date_created')
    date_expire = models.DateTimeField('date_expire', default=datetime.datetime.now() + datetime.timedelta(weeks=1))
    total_votes = models.IntegerField(default=0)

    def results(self):
        return [ (c.choice, c.votes) for c in self.choice_set.all()]

    def has_expired(self):
        return self.date_expire < datetime.datetime.now()

    @models.permalink
    def get_absolute_url(self):
        return ('polls.views.view', (), {'poll_id':self.id})

    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __unicode__(self):
        return self.choice

class Vote(models.Model):
    poll = models.ForeignKey(Poll)
    hash = models.CharField(max_length=32)

    def __unicode__(self):
        return self.hash
