from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from polls.models import Poll
import polls
import haystack
import haystack.views

about_view = TemplateView.as_view(template_name='about.html')

urlpatterns = patterns('',
    url(r'^$','polls.views.index', name = 'index_view'),
    url(r'^(?P<poll_id>\d+)/$', 'polls.views.view', name = 'poll_view'),
    url(r'^create$', 'polls.views.create'),
    url(r'^about$', about_view),
    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),

    # Search page(s)
    url(r'^search/',
        haystack.views.search_view_factory(
            view_class=haystack.views.SearchView,
            template='search.html',
            form_class=haystack.forms.SearchForm
        ),
        name='search'),
)
