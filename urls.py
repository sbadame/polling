from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from polls.models import Poll

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Poll.objects.order_by("-date_created"),
            context_object_name='latest_poll_list',
            template_name='pollstemplate/index.html')),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Poll,
            template_name='pollstemplate/detail.html'),
        name = 'poll_view'),
    url(r'^(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Poll,
            template_name='pollstemplate/results.html'),
        name='poll_results'),
    url(r'^create$', 'polls.views.create'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
)
