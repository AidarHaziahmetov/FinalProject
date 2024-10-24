import django_filters
from django.db.models import Q
from django_filters import FilterSet

from shop.models import Product


class ProductFilter(FilterSet):
    price_range = django_filters.RangeFilter(field_name='price',label='Цена от и до')
    available = django_filters.BooleanFilter(method='filter_available', label='В наличии')
    term = django_filters.CharFilter(method='filter_term', label='Поиск по названию и описанию')
    class Meta:
        model = Product
        fields = ['term','category','available','price_range', 'brand']

    def filter_available(self, queryset, name, value):
        if value is None:
            return queryset
        elif value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)

    def filter_term(self, queryset, name, value):
        criteria = Q()
        for term in value.split():
            criteria &= Q(name__icontains=term)|Q(description__icontains=term)
        return queryset.filter(criteria).distinct()