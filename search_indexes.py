import datetime
from haystack import indexes
from polls.models import Poll

class PollIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='question', document=True, use_template=True)
    date_created = indexes.DateTimeField(model_attr='date_created')
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Poll

    def index_queryset(self):
        return self.get_model().objects.filter(date_created__lte=datetime.datetime.now())

