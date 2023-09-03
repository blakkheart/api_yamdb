from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """FilterSet class that allows to filter Title class.
    Can filter via name, year, genre, category fields.
    """

    name = filters.CharFilter(field_name='name', lookup_expr='iexact')
    year = filters.NumberFilter(field_name='year', lookup_expr='iexact')
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='iexact')
    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
