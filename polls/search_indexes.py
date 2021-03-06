import datetime
from haystack.indexes import *
from haystack import site
from polls.models import Public_Poll

class Public_PollIndex(SearchIndex):
    text = CharField(model_attr='question', document=True, use_template=True)
    date_created = DateTimeField(model_attr='date_created')
    choices = MultiValueField()

    def get_model(self):
        return Public_Poll

    def prepare_choices(self, obj):
        return obj.choice_set.values_list('choice', flat=True)

    def index_queryset(self):
        return self.get_model().objects.filter(date_created__lte=datetime.datetime.now())

site.register(Public_Poll, Public_PollIndex)
