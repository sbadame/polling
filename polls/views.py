from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.core.urlresolvers import reverse
from polls.models import Poll,Public_Poll,Private_Poll,Choice,Vote,RandomPollPick,NewestPollPick,MostVotedPollPick,PopularPollPick
from django.views.decorators.cache import cache_page
import datetime
import haystack
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
    #Test whether we actually got a question
    if 'question' not in request.POST or not request.POST['question'].strip():
        return render_to_response(\
            'index.html',\
            {'error_message':"You did not supply a question"},\
            context_instance = RequestContext(request))

    question = request.POST['question'].strip()

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
            return HttpResponseRedirect(reverse('poll_view',args=(p.id,)))

def view(request, poll_id):
    poll = get_object_or_404(Public_Poll, pk=poll_id)
    return render_to_response("results.html", {'poll' : poll}, context_instance=RequestContext(request))

def view_private(request, private_hash):
    poll = get_object_or_404(Private_Poll, private_hash=private_hash)
    return render_to_response("results.html", {'poll' : poll}, context_instance=RequestContext(request))

def get_random_poll():
    from settings import NUMBER_OF_RANDOM_POLLS
    import random
    index = random.randint(0, NUMBER_OF_RANDOM_POLLS - 1)
    return RandomPollPick.objects.get(index=index).poll

#@cache_page(60 * 15) #Only update the index page every 15 minutes... nice...
def index(request):
    now = datetime.datetime.now()
    latest_poll = [x.poll for x in NewestPollPick.objects.all()][0]
    mostvoted_poll = [x.poll for x in MostVotedPollPick.objects.all()][0]
    hottest_poll = [x.poll for x in PopularPollPick.objects.all()][0]
    random_poll = get_random_poll()
    template = "index.html"
    return render_to_response(template,
            {'latest_poll': latest_poll,
             'mostvoted_poll': mostvoted_poll,
             'random_poll': random_poll,
             'hottest_poll': hottest_poll
            },
            context_instance=RequestContext(request))

def vote_public(request, poll_id):
    poll = get_object_or_404(Public_Poll, pk=poll_id)
    result = vote(request,poll)
    if result:
        return result
    return HttpResponseRedirect(reverse('poll_view',args=(poll.id,)))

def vote_private(request, private_hash):
    poll = get_object_or_404(Private_Poll, private_hash=private_hash)
    result = vote(request,poll)
    if result:
        return result
    return HttpResponseRedirect(reverse('private_view',args=(poll.private_hash,)))

def vote(request, poll):
    try:
        choice_name = request.POST['choice']
        selected_choice = poll.choice_set.get(choice=choice_name)
    except (KeyError, Choice.DoesNotExist):
        return render_to_response('detail.html', {'poll':poll, 'error_message':"You didn't select a choice."},
                context_instance= RequestContext(request))

    if not (poll.has_expired() or already_voted(request, poll)):
        hash = request_hash(request)
        poll.total_votes += 1
        selected_choice.votes += 1
        poll.vote_set.create(hash=hash)
        selected_choice.save()

        #Update the seen ips
        from pybloomfilter import BloomFilter
        bf = BloomFilter.from_base64('/tmp/bloom.filter', poll.ips_seen)
        alreadyseen = bf.add(request.META['REMOTE_ADDR'])

        if not alreadyseen:
            poll.ips_seen = bf.to_base64()
            poll.ips_count += 1

        poll.save()

    return None
