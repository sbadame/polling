from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from polls.models import Poll
import polls
import haystack
import haystack.views

about_view = TemplateView.as_view(template_name='about.html')
contact_view = TemplateView.as_view(template_name='contact.html')
#search = TemplateView.as_view(template_name='search.html')

urlpatterns = patterns('',
    url(r'^$','polls.views.index', name = 'index_view'),
    url(r'^(?P<poll_id>\d+)/$', 'polls.views.view', name = 'poll_view'),
    url(r'^create$', 'polls.views.create'),
    url(r'^about$', about_view),
    url(r'^contact$', contact_view),
    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote_public'),
    url(r'^private/(?P<private_hash>[a-zA-Z0-9]+)/$', 'polls.views.view_private', name = 'private_view'),
    url(r'^private/(?P<private_hash>[a-zA-Z0-9]+)/vote/$', 'polls.views.vote_private'),

    # Search page(s)
    url(r'^search/',
        haystack.views.search_view_factory(
            view_class=haystack.views.SearchView,
            template='search.html',
            form_class=haystack.forms.SearchForm
        ),
        name='search'),
)
