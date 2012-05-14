
from django.core.management.base import BaseCommand, CommandError
from polls.models import Public_Poll
from polls.models import RandomPollPick
from datetime import datetime
from settings import NUMBER_OF_RANDOM_POLLS as NUMBER_OF_POLLS

class Command(BaseCommand):
    args = '<none>'
    help = 'Updates the list of random polls'

    def handle(self, *args, **options):
        picks = Public_Poll.objects.exclude(date_expire__lt=datetime.now()).order_by('?')[:NUMBER_OF_POLLS]
        for index, pick in enumerate(picks):

            #Get rid of the old index for this poll if it exists
            try:
                oldentry = RandomPollPick.objects.get(poll=pick)
                oldentry.delete()
            except RandomPollPick.DoesNotExist:
                pass

            try:
                randomEntry = RandomPollPick.objects.get(index=index)
                randomEntry.poll = pick
            except RandomPollPick.DoesNotExist:
                randomEntry = RandomPollPick.objects.create(index=index, poll=pick)

            randomEntry.save()

