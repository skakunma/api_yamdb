from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter
from reviews.models import Title


class TitleFilter(FilterSet):
    name = CharFilter(field_name='name',)
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year',)
