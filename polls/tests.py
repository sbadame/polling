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

        self.new_poll = Poll.create("New Poll", "Choice1", "Choice2", "Choice3")

        #An expired poll
        self.expiration_length = Poll.time_delta_to_expire + datetime.timedelta(days=1)
        self.expired_poll = Poll.create("Expired Poll", "Choice1", "Choice2", "Choice3",
                date_created=datetime.datetime.now() - self.expiration_length)

    def test_create(self):
        question = "A Generic Name"
        choice1 = "A Choice"
        choice2 = "A Second Choice"
        poll = Poll.create(question, choice1, choice2)

        self.assertEqual(question, poll.question)

    def test_new_poll_has_expired(self):
        self.assertFalse(self.new_poll.has_expired())

    def test_expired_poll_has_expired(self):
        self.assertTrue(
                self.expired_poll.has_expired(),
                "%s has not expired. length=%s" % (self.expired_poll, self.expiration_length))
