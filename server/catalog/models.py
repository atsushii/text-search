import uuid

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchQuery, SearchRank

from django.db import models
from django.db.models import F, Q


class WineQuerySet(models.query.QuerySet):
    def search(self, query):
        search_query = Q(
            Q(search_vector=SearchQuery(query))
        )
        return self.annotate(
            variety_headline=SearchHeadLine(F('variety'), SearchQuery(query)),
            winery_headline=SearchHeadLine(F('winery'), SearchQuery(query)),
            description_headline=SearchHeadLine(F('description'), SearchQuery(query)),
            search_rank=SearchRank(F('search_vector'), SearchQuery(query)),
        ).filter(search_query).order_by('-search_rank', 'id')


class Wine(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    country = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    points = models.IntegerField()
    price = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True
    )
    variety = models.CharField(max_length=255)
    winery = models.CharField(max_length=255)
    search_vector = SearchVectorField(null=True, blank=True)

    objects = WineQuerySet.as_manager()

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'], name='search_index')
        ]

    def __str__(self):
        return f'{self.id}'


class SearchHeadLine(models.Func):
    function = 'ts_headline'
    output_field = models.TextField()
    template = '%(function)s(%(expressions)s, \'StartSel = <mark>, StopSel = </mark>, HighlightAll=TRUE\')'