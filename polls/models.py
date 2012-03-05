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
    time_delta_to_expire = datetime.timedelta(weeks=1)
    question = models.CharField(max_length=200)
    date_created = models.DateTimeField('date_created', default=datetime.datetime.now())
    date_expire = models.DateTimeField(
            'date_expire',
            default = datetime.datetime.now() + time_delta_to_expire)
    total_votes = models.IntegerField(default=0)

    @staticmethod
    def create(question, *choices, **kwargs):
        """ Such a pain, I want the expiration time to be a function of the creation time. But nooooooooooooo.
        Time for some design patterns up in this bitch. Factory method: GO!!"""

        if not question or not choices:
            raise ValueError("Both question: %s and choices: %s must be defined" % (question, choices))

        if len(choices) < 2:
            raise ValueError("Poll can't have less than two choices: %s" % choices)

        if "question" in kwargs:
            raise ValueError("Can't define question twice arg: \"%s\", question=\"%s\"" % (question,
                kwargs["question"]))

        if "date_created" not in kwargs:
            kwargs["date_created"] = datetime.datetime.now()

        if "date_expire" not in kwargs:
            kwargs["date_expire"] = kwargs["date_created"] + Poll.time_delta_to_expire

        newpoll = Poll.objects.create(question=question, **kwargs)

        for choice in choices:
            newpoll.choice_set.create(choice=choice, votes=0)

        return newpoll

    def results(self):
        return [ (c.choice, c.votes) for c in self.choice_set.all()]

    def has_expired(self):
        return self.date_expire < datetime.datetime.now()

    @models.permalink
    def get_absolute_url(self):
        return ('polls.views.view', (), {'poll_id':self.id})

    def __unicode__(self):
        return "%s(id=%d,question=\"%s\",expires=%s)" % (
            self.__class__.__name__,
            self.id,
            self.question,
            self.date_expire)

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
