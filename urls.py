from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from polls.models import Poll
import polls

poll_view_function = DetailView.as_view( model=Poll, template_name='detail.html')
index_view_function = ListView.as_view(
        queryset=Poll.objects.order_by("-date_created")[:10],
            context_object_name='latest_poll_list',
            template_name='index.html')


urlpatterns = patterns('',
    url(r'^$',index_view_function),
    url(r'^(?P<pk>\d+)/$', poll_view_function, name = 'poll_view'),
    url(r'^(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Poll,
            template_name='results.html'),
        name='poll_results'),
    url(r'^create$', 'polls.views.create'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
)
