"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

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
        #Next two methods should throw an exception if the choice doesn't exist.
        poll.choice_set.get(choice=choice1)
        poll.choice_set.get(choice=choice2)
        self.assertEqual(2, poll.choice_set.count())

    def test_new_poll_has_expired(self):
        self.assertFalse(self.new_poll.has_expired())

    def test_expired_poll_has_expired(self):
        self.assertTrue(
                self.expired_poll.has_expired(),
                "%s has not expired. length=%s" % (self.expired_poll, self.expiration_length))

class PollViewTestCase(TestCase):
    """ Time to test the views """

    def test_successful_create(self):
        c = Client()
        question = 'My new question'
        choice1 = "dog"
        choice2 = "cat"
        response = c.post('/create', {'question': question, 'choice1': choice1, 'choice2' : choice2 })

        #Since this is a form submission, redirect is good practice. So 302 not 200 is the correct response
        self.assertEquals(302, response.status_code)

    def test_successful_view(self):
        p = Poll.create("New Poll", "Choice1", "Choice2")
        c = Client()

        response = c.get("/"+str(p.id)+"/", HTTP_USER_AGENT="django-test", REMOTE_ADDR="0.0.0.0")
        self.assertEquals(200, response.status_code)
        self.assertEquals(p, response.context['poll'])



















