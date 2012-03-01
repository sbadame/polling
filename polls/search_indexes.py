import datetime
from haystack.indexes import *
from haystack import site
from polls.models import Poll

class PollIndex(SearchIndex):
    text = CharField(model_attr='question', document=True, use_template=True)
    date_created = DateTimeField(model_attr='date_created')
    suggestions = FacetCharField()

    def get_model(self):
        return Poll

    def index_queryset(self):
        return self.get_model().objects.filter(date_created__lte=datetime.datetime.now())

site.register(Poll, PollIndex)
