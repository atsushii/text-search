from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchVector

from django_filters.rest_framework import CharFilter, FilterSet

from .models import Wine


class WineFilterSet(FilterSet):
    query = CharFilter(method='filter_query')

    def filter_query(self, queryset, name, value):
        search_query = Q(
            Q(search_vector=SearchQuery(value))
        )
        return queryset.annotate(
            search_vector=SearchVector('variety', 'winery', 'description')
        ).filter(search_query)

    class Meta:
        model = Wine
        fields = ('query', 'country', 'points',)
