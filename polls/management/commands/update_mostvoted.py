
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from polls.models import Public_Poll, MostVotedPollPick
from settings import NUMBER_OF_RANDOM_POLLS as NUMBER_OF_POLLS

class Command(BaseCommand):
    args = '<none>'
    help = 'Updates the list of most voted polls'

    def handle(self, *args, **options):
        #Wipe out the table
        #TODO(sandro): turn this into a drop table
        for pick in MostVotedPollPick.objects.all(): pick.delete()

        picks = Public_Poll.objects.exclude(date_expire__lt=datetime.now()).order_by('-total_votes')[:NUMBER_OF_POLLS]

        for index, poll in enumerate(picks):
            MostVotedPollPick.objects.create(index=index, poll=poll).save()

