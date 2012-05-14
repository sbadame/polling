
from django.core.management.base import BaseCommand, CommandError
from polls.models import Public_Poll
from polls.models import RandomPollList
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
                oldentry = RandomPollList.objects.get(poll=pick)
                oldentry.delete()
            except RandomPollList.DoesNotExist:
                pass

            try:
                randomEntry = RandomPollList.objects.get(index=index)
                randomEntry.poll = pick
            except RandomPollList.DoesNotExist:
                randomEntry = RandomPollList.objects.create(index=index, poll=pick)

            randomEntry.save()

