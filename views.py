from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from polls.models import Poll,Choice,Vote

import hashlib

# def index(request):
#     latest_poll_list = Poll.objects.all().order_by('-date_created')[:5]
#     return render_to_response("polls/index.html", {'latest_poll_list': latest_poll_list})
# 
# def detail(request, poll_id):
#     p = get_object_or_404(Poll, pk=poll_id)
#     return render_to_response("polls/detail.html", {'poll': p}, context_instance=RequestContext(request))
# 
# def results(request, poll_id):
#     p = get_object_or_404(Poll, pk=poll_id)
#     return render_to_response("polls/results.html", {'poll': p})
# 

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
        if choice:
            choices.append(choice)
        index += 1

    if not choices or len(choices) < 2:
        return render_to_response(\
            'index.html',\
            {'error_message':"You did not supply enough choices"},\
            context_instance = RequestContext(request))
    else:
        p = Poll(question=question, date_created=datetime.now())
        p.save()
        for choice in choices:
            p.choice_set.create(choice=choice, votes=0)
        return HttpResponseRedirect(reverse('poll_view',args=(p.id,)))


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render_to_response('detail.html', {'poll':p, 'error_message':"You didn't select a choice."},
                context_instance= RequestContext(request))

    hasher = hashlib.md5()
    hasher.update(request.META['REMOTE_ADDR'])
    hasher.update(request.META['HTTP_USER_AGENT'])
    hash = hasher.hexdigest()
    try:
        vote = p.vote_set.get(hash=hash)
    except Vote.DoesNotExist:
        selected_choice.votes += 1
        selected_choice.save()
        p.vote_set.create(hash=hash)

    return HttpResponseRedirect(reverse('poll_results',args=(p.id,)))
