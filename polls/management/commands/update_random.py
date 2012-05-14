from django.core.management.base import BaseCommand, CommandError
from polls.models import Public_Poll

class Command(BaseCommand):
    args = '<none>'
    help = 'Updates the list of random polls'

    def handle(self, *args, **options):
        self.stdout.write("Hello world\n")
