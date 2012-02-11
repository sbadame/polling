from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from polls.models import Poll
import polls

#index_view_function = ListView.as_view(
#        queryset=Poll.objects.order_by("-date_created")[:10],
#            context_object_name='latest_poll_list',
#            template_name='index.html')

about_view = TemplateView.as_view(template_name='about.html')
contact_view = TemplateView.as_view(template_name='contact.html')

urlpatterns = patterns('',
    url(r'^$','polls.views.index', name = 'index_view'),
    url(r'^(?P<poll_id>\d+)/$', 'polls.views.view', name = 'poll_view'),
    url(r'^create$', 'polls.views.create'),
    url(r'^about$', about_view),
    url(r'^contact$', contact_view),
    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
)
