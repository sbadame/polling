
from django.core.management.base import BaseCommand, CommandError
from polls.models import Public_Poll
import random

QUESTION_POOL_FILE = "polls/management/commands/questions.txt"
CHOICES_POOL_FILE = "polls/management/commands/choices.txt"

def create_random_polls(howmany):
    Command().handle(howmany)

class Command(BaseCommand):
    args = '<number of polls>'
    help = 'Generates a number of random giberish Pubic Polls'

    def handle(self, *args, **options):
        try:
            number_to_generate = int(args[0])
        except:
            print("Pass in the the number of polls to generate")
            return

        print("Generating %d polls..." % number_to_generate)

        question_pool = [x.strip() for x in file(QUESTION_POOL_FILE).readlines()]
        choices_pool = [x.strip() for x in file(CHOICES_POOL_FILE).readlines()]

        for _ in range(number_to_generate):
            question = random.choice(question_pool)
            choices = random.sample(choices_pool, random.randint(2,5))
            poll = Public_Poll.create(question, *choices)
            print(poll)

        print("Generated %d polls." % number_to_generate)

