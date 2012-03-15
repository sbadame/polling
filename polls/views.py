from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.core.urlresolvers import reverse
from polls.models import Poll,Public_Poll,Private_Poll,Choice,Vote
from django.views.decorators.cache import cache_page
import datetime
import haystack
import random
import hashlib
from django.views.decorators.csrf import csrf_protect, csrf_exempt

def request_hash(request):
    hasher = hashlib.md5()
    hasher.update(request.META['REMOTE_ADDR'])
    hasher.update(request.META['HTTP_USER_AGENT'])
    return hasher.hexdigest()

def already_voted(request, poll):
    hash = request_hash(request)
    return poll.vote_set.filter(hash__exact=hash).exists()

def create(request):
    try:
        question = request.POST['question'].strip()
        if not question:
            raise KeyError("No question supplied")
    except KeyError:
        return render_to_response(\
            'index.html',\
            {'error_message':"You did not supply a question"},\
            context_instance = RequestContext(request))

    choices = []
    index = 1
    while True:
        try:
            choice = request.POST['choice'+str(index)].strip()
        except KeyError:
            break
        if choice[:6] == 'Choice':
            index += 1
            continue
        if choice:
            choices.append(choice)
        index += 1

    if not choices or len(choices) < 2:
        return render_to_response(\
            'index.html',\
            {'error_message':"You did not supply enough choices"},\
            context_instance = RequestContext(request))
    else:
        if request.POST['pub_priv'] == 'Private':
            p = Private_Poll.create(question, *choices)
            return HttpResponseRedirect(reverse('private_view',args=(p.private_hash,)))
        else:
            p = Public_Poll.create(question, *choices)
            #p = Poll(question=question, date_created=datetime.datetime.now())
            #p.save()
            #for choice in choices:
                #p.choice_set.create(choice=choice, votes=0)
            return HttpResponseRedirect(reverse('poll_view',args=(p.id,)))

def view(request, poll_id):
    poll = get_object_or_404(Public_Poll, pk=poll_id)
    if poll.has_expired() or already_voted(request, poll):
        template = "results.html"
    else:
        template = "detail.html"
    return render_to_response(template, {'poll' : poll}, context_instance=RequestContext(request))

def view_private(request, private_hash):
    poll = get_object_or_404(Private_Poll, private_hash=private_hash)
    if poll.has_expired() or already_voted(request, poll):
        template = "results.html"
    else:
        template = "detail.html"
    return render_to_response(template, {'poll' : poll}, context_instance=RequestContext(request))

def get_random_poll():
    #In a perfect world, just picking a number from 0 -  Poll.objects.count() would work. Sadly
    #polls get deleted. (Like poll 11 on my computer doesn't exist...)
    #OK so we need a random, poll. Django gives us something for that: *.order_by('?'). Too bad
    #its performance is utter garbage on mysql.
    #So lets take the perro approach but wrap it a while loop to make sure that our id actually exists.
    #TODO: make this handle the case of a sparse database better. (Or maybe it should encourage dense DBs)

    poll_count = Poll.objects.count()
    while True:
        rand_poll_id = random.randint(1,poll_count-1)
        try:
            random_poll = Poll.objects.get(id=rand_poll_id)
            return random_poll
        except Poll.DoesNotExist:
            #Darn it! Got a row that doesn't exist... try again...
            pass


@cache_page(60 * 15) #Only update the index page every 15 minutes... nice...
def index(request):
    latest_poll_list = Public_Poll.objects.all().order_by('-date_created')[:10]
    popular_poll_list = Public_Poll.objects.order_by('-total_votes')[:10]
    danger_poll_list = Public_Poll.objects.filter(date_expire__gt=datetime.datetime.now()).order_by('date_expire')[:10]
    random_poll = get_random_poll()
    template = "index.html"
    return render_to_response(template, {'latest_poll_list': latest_poll_list,'popular_poll_list': popular_poll_list,
        'random_poll': random_poll,'danger_poll_list': danger_poll_list}, context_instance=RequestContext(request))

def vote_public(request, poll_id):
    p = get_object_or_404(Public_Poll, pk=poll_id)
    vote(request,p)
    return HttpResponseRedirect(reverse('poll_view',args=(p.id,)))

def vote_private(request, private_hash):
    p = get_object_or_404(Private_Poll, private_hash=private_hash)
    vote(request,p)
    return HttpResponseRedirect(reverse('private_view',args=(p.private_hash,)))

def vote(request, p):
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render_to_response('detail.html', {'poll':p, 'error_message':"You didn't select a choice."},
                context_instance= RequestContext(request))

    if not (p.has_expired() or already_voted(request, p)):
        hash = request_hash(request)
        p.total_votes += 1
        selected_choice.votes += 1
        p.vote_set.create(hash=hash)
        selected_choice.save()
        p.save()
