from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from polls.models import Public_Poll, PopularPollPick
from settings import NUMBER_OF_RANDOM_POLLS as NUMBER_OF_POLLS
from math import log10 as log

#From reddit: http://amix.dk/blog/post/19588
#https://github.com/reddit/reddit/blob/master/r2/r2/lib/db/_sorts.pyx

epoch = datetime(1970, 1, 1)
def popular_score(poll):
    popularity = log(poll.total_votes) if poll.total_votes else 0
    return  popularity + (poll.date_created - epoch).total_seconds()

class Command(BaseCommand):
    args = '<none>'
    help = 'Updates the list of most popular polls'

    def handle(self, *args, **options):
        #Wipe out the table
        #TODO(sandro): turn this into a drop table
        for pick in PopularPollPick.objects.all(): pick.delete()

        picks = list(Public_Poll.objects.exclude(date_expire__lt=datetime.now()).all())
        picks.sort(key=popular_score, reverse=True) #We want descending order
        picks = picks[:NUMBER_OF_POLLS]

        for poll in picks:
            PopularPollPick.objects.create(score=popular_score(poll), poll=poll).save()

