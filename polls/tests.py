"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from polls.models import Poll
import datetime

class PollTestCase(TestCase):
    def setUp(self):

        # Plain old new poll
        self.new_poll = Poll.create(
                question="New Poll",
                date_created=datetime.datetime.now())
        self.new_poll.choice_set.create(choice="Choice1", votes=0)
        self.new_poll.choice_set.create(choice="Choice2", votes=0)
        self.new_poll.choice_set.create(choice="Choice3", votes=0)

        #An expired poll
        self.expiration_length = Poll.time_delta_to_expire + datetime.timedelta(days=1)
        self.expired_poll = Poll.create(
                question="Expired Poll",
                date_created=datetime.datetime.now() - self.expiration_length)
        self.expired_poll.choice_set.create(choice="Choice1", votes=0)
        self.expired_poll.choice_set.create(choice="Choice2", votes=0)
        self.expired_poll.choice_set.create(choice="Choice3", votes=0)

    def test_new_poll_has_expired(self):
        self.assertFalse(self.new_poll.has_expired())

    def test_expired_poll_has_expired(self):
        self.assertTrue(
                self.expired_poll.has_expired(),
                "%s has not expired. length=%s" % (self.expired_poll, self.expiration_length))
