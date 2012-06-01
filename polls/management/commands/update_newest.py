
from django.core.management.base import BaseCommand, CommandError
from polls.models import Public_Poll
from polls.models import NewestPollPick
from datetime import datetime
from settings import NUMBER_OF_RANDOM_POLLS as NUMBER_OF_POLLS

class Command(BaseCommand):
    args = '<none>'
    help = 'Updates the list of newest polls'

    def handle(self, *args, **options):
        #Wipe out the table
        #TODO(sandro): turn this into a drop table
        for pick in NewestPollPick.objects.all(): pick.delete()

        picks = Public_Poll.objects.exclude(date_expire__lt=datetime.now()).order_by('-date_created')[:NUMBER_OF_POLLS]

        for index, poll in enumerate(picks):
            NewestPollPick.objects.create(index=index, poll=poll).save()

