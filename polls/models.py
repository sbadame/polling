import datetime
from django.db import models
import hashlib

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


class Public_Poll(Poll):
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

        newpoll = Public_Poll.objects.create(question=question, **kwargs)

        for choice in choices:
            newpoll.choice_set.create(choice=choice, votes=0)

        return newpoll

    public_hash = models.IntegerField(default=0)

    @models.permalink
    def get_vote_url(self):
        return ('polls.views.vote_public', (), {'poll_id':self.id})

class Private_Poll(Poll):

    private_hash = models.CharField(max_length=200)

    @models.permalink
    def get_absolute_url(self):
        return ('polls.views.view_private', (), {'private_hash':self.private_hash})

    @models.permalink
    def get_vote_url(self):
        return ('polls.views.vote_private', (), {'private_hash':self.private_hash})

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

        if "private_hash" not in kwargs:
            hasher = hashlib.md5()
            hasher.update(question)
            time_hash = datetime.datetime.now()
            hasher.update(str(time_hash))
            base16 = hasher.hexdigest()
            kwargs["private_hash"] = Private_Poll.convertBase16ToBase62(base16)

        newpoll = Private_Poll.objects.create(question=question, **kwargs)

        for choice in choices:
            newpoll.choice_set.create(choice=choice, votes=0)

        return newpoll

    @staticmethod
    def convertBase16ToBase62(base16str):
        """
        Maybe Perro math can clean this up.
        Convert to base 10, convert to base 62
        Mostly snagged from:
        http://code.activestate.com/recipes/111286-numeric-base-converter-that-accepts-arbitrary-digi/
        """
        import string
        base62 = string.digits + string.ascii_lowercase + string.ascii_uppercase
        base16 = string.digits + "abcdef"
        base16str = base16str.lower()

        #Convert to base10
        base10num = 0
        for digit in base16str:
            base10num = base10num*16 + base16.index(digit)

        #Convert to base62
        result = ""
        while base10num > 0:
            digit = base10num % 62
            result = base62[digit] + result
            base10num /= 62

        return result if result else "0"


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
