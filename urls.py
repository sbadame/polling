from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from polls.models import Poll
import polls

index_view_function = ListView.as_view(
        queryset=Poll.objects.order_by("-date_created")[:10],
            context_object_name='latest_poll_list',
            template_name='index.html')

urlpatterns = patterns('',
    url(r'^$',index_view_function),
    url(r'^(?P<poll_id>\d+)/$', 'polls.views.view', name = 'poll_view'),
    url(r'^create$', 'polls.views.create'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
)
