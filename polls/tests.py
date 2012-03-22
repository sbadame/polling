"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from polls.models import Public_Poll
from polls.models import Private_Poll
import datetime

class PollTestCase(TestCase):

    def setUp(self):
        self.new_poll = Public_Poll.create("New Poll", "Choice1", "Choice2", "Choice3")

        #An expired poll
        self.expiration_length = Public_Poll.time_delta_to_expire + datetime.timedelta(days=1)
        self.expired_poll = Public_Poll.create("Expired Poll", "Choice1", "Choice2", "Choice3",
                date_created=datetime.datetime.now() - self.expiration_length)

    def test_create(self):
        question = "A Generic Name"
        choice1 = "A Choice"
        choice2 = "A Second Choice"
        poll = Public_Poll.create(question, choice1, choice2)

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

class AnyPollViewTests(object):
    '''Notice that this class doesn't subclass TestCase.
    Here we store all tests that are relevent to both types of polls
    Public and Private. Subclasses just need to return w/e class they
    want to be tested with this suite of tests. See Private_PollViewTests
    and Public_PollViewTests to see how they use this class.'''
    #TODO: Add test cases for when things go horribly wrong
    #TODO: Add test cases for cheating

    def test_successful_view(self):
        url = self.poll.get_absolute_url()
        response = self.client.get(url, HTTP_USER_AGENT="django-test", REMOTE_ADDR="0.0.0.0")
        self.assertEquals(200, response.status_code)
        self.assertEquals(self.poll, response.context['poll'])

    def test_successful_vote(self):
        choice =  self.poll.choice_set.all()[0]
        c = Client()
        response = c.post(self.poll.get_vote_url(), {"choice":choice.id}, HTTP_USER_AGENT="django-test", REMOTE_ADDR="0.0.0.0")

        #Need to reload poll from the db, the "cached" p.total_votes is different now.
        #Don't know of how else to do it...
        p = self.getPollModelClass().objects.get(pk=self.poll.id)
        self.assertEquals(302, response.status_code)
        self.assertEquals(1, p.choice_set.get(pk=choice.id).votes)
        self.assertEquals(1, p.total_votes)

    def test_empty_post_vote(self):
        response = self.client.post(self.poll.get_vote_url(), {}, HTTP_USER_AGENT="django-test", REMOTE_ADDR="0.0.0.0")

        self.poll = self.getPollModelClass().objects.get(pk=self.poll.id)
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, self.poll.total_votes)
        for choice in self.poll.choice_set.all():
            self.assertEquals(0, choice.votes)

    def test_empty_question_create(self):
        response = self.client.post('/create',
                {'question':"  ", 'Choice1':'sup', 'Choice2':'dog', 'pub_priv':''})
        self.assertEquals(200, response.status_code)

class Private_PollViewTests(TestCase, AnyPollViewTests):

    def setUp(self):
        self.poll = self.getPollModelClass().create("New Poll", "Choice1", "Choice2")
        self.client = Client()

    def getPollModelClass(self):
        return Private_Poll

    # This needs to be its own function since the post parameters between Public and Private polls
    # are different
    def test_successful_private_create(self):
        question = 'My new question'
        choice1 = "dog"
        choice2 = "cat"
        response = self.client.post('/create', {'question': question, 'choice1': choice1, 'choice2' : choice2, 'pub_priv':
        'Private' })

        #Since this is a form submission, redirect is good practice. So 302 not 200 is the correct response
        self.assertEquals(302, response.status_code)


class Public_PollViewTests(TestCase, AnyPollViewTests):

    def setUp(self):
        self.poll = self.getPollModelClass().create("New Poll", "Choice1", "Choice2")
        self.client = Client()

    def getPollModelClass(self):
        return Public_Poll

    # This needs to be its own function since the post parameters between Public and Private polls
    # are different
    def test_successful_public_create(self):
        question = 'My new question'
        choice1 = "dog"
        choice2 = "cat"
        response = self.client.post('/create', {'question': question, 'choice1': choice1, 'choice2' : choice2, 'pub_priv': '' })

        #Since this is a form submission, redirect is good practice. So 302 not 200 is the correct response
        self.assertEquals(302, response.status_code)

    def test_successful_public_view(self):
        self.do_successful_view(Public_Poll)

    def test_successful_private_view(self):
        self.do_successful_view(Private_Poll)

    def do_successful_view(self, polltype):
        p = polltype.create("New Poll", "Choice1", "Choice2")
        c = Client()
        url = p.get_absolute_url()
        response = c.get(url, HTTP_USER_AGENT="django-test", REMOTE_ADDR="0.0.0.0")
        self.assertEquals(200, response.status_code)
        self.assertEquals(p, response.context['poll'])

    def test_successful_vote(self):
        p = self.getPollModelClass().create("New Poll", "Choice1", "Choice2")
        choice =  p.choice_set.all()[0]
        c = Client()
        response = c.post(p.get_vote_url(), {"choice":choice.id}, HTTP_USER_AGENT="django-test", REMOTE_ADDR="0.0.0.0")

        #Need to reload poll from the db, the "cached" p.total_votes is different now.
        #Don't know of how else to do it...
        p = self.getPollModelClass().objects.get(pk=p.id)
        self.assertEquals(302, response.status_code)
        self.assertEquals(1, p.choice_set.get(pk=choice.id).votes)
        self.assertEquals(1, p.total_votes)

class Private_PollViewTests(TestCase, AnyPollViewTests):

    def getPollModelClass(self):
        return Private_Poll

    # This needs to be its own function since the post parameters between Public and Private polls
    # are different
    def test_successful_private_create(self):
        c = Client()
        question = 'My new question'
        choice1 = "dog"
        choice2 = "cat"
        response = c.post('/create', {'question': question, 'choice1': choice1, 'choice2' : choice2, 'pub_priv':
        'Private' })

        #Since this is a form submission, redirect is good practice. So 302 not 200 is the correct response
        self.assertEquals(302, response.status_code)


class Public_PollViewTests(TestCase, AnyPollViewTests):

    def getPollModelClass(self):
        return Public_Poll

    # This needs to be its own function since the post parameters between Public and Private polls
    # are different
    def test_successful_public_create(self):
        c = Client()
        question = 'My new question'
        choice1 = "dog"
        choice2 = "cat"
        response = c.post('/create', {'question': question, 'choice1': choice1, 'choice2' : choice2, 'pub_priv': '' })

        #Since this is a form submission, redirect is good practice. So 302 not 200 is the correct response
        self.assertEquals(302, response.status_code)
