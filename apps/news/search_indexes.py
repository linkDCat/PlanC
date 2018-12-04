#-*- conding:utf-8 -*-
from .models import News
from haystack import indexes

class NewsIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.all()