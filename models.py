from django.db import models

# Create your models here.

class Poll(models.Model):
    question = models.CharField(max_length=20)
    date_created = models.DateTimeField('date_created')
    date_expire = models.DateTimeField('date_expire', null=True)

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
