import django_filters
from django import forms
from django.db.models import Q
from django_filters import FilterSet, widgets

from shop import models
class CustomSelectWidget(forms.Select):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'form-select'})

class MyRangeWidget(widgets.RangeWidget):
    def __init__(self, from_attrs=None, to_attrs=None, attrs=None):
        super(MyRangeWidget, self).__init__(attrs)
        if from_attrs:
            self.widgets[0].attrs.update(from_attrs)
        if to_attrs:
            self.widgets[1].attrs.update(to_attrs)

class ProductFilter(FilterSet):
    price_range = django_filters.RangeFilter(field_name='price', label='Цена',
                                             widget=MyRangeWidget(from_attrs={'placeholder':'От'}, to_attrs={'placeholder':'До'}, attrs={'class': 'form-control'}))
    available = django_filters.BooleanFilter(method='filter_available', label='В наличии',
                                             widget=forms.NullBooleanSelect(attrs={'class': 'form-control'}))
    term = django_filters.CharFilter(method='filter_term', label='Поиск по названию и описанию',
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    brand = django_filters.ModelChoiceFilter(field_name='brand', label='Бренд', queryset=models.Brand.objects.all(),
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    category = django_filters.ModelMultipleChoiceFilter(field_name='category', label='Категории',
                                                        queryset=models.Category.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple, method='filter_category')
    order_by = django_filters.OrderingFilter(
        fields=(('price', 'price'), ('-price', '-price'),),
        widget=CustomSelectWidget,
        label='Сортировка по цене',
        choices=[
            ('price', 'По возрастанию'),
            ('-price', 'По убыванию'),
        ],
    )

    class Meta:
        model = models.Product
        fields = ['term', 'category', 'available', 'price_range', 'brand']

    def filter_available(self, queryset, name, value):
        if value is None:
            return queryset
        elif value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)

    def filter_term(self, queryset, name, value):
        criteria = Q()
        for term in value.split():
            criteria &= Q(name__icontains=term) | Q(description__icontains=term)
        return queryset.filter(criteria).distinct()

    def filter_category(self, queryset, name, value):
        if value:
            categories = []
            for category_id in value:
                category = models.Category.objects.get(pk=category_id.id)
                categories.extend(category.get_all_children())  # Используйте get_all_children()

            # Добавьте саму выбранную категорию
            categories.extend(value)
            queryset = queryset.filter(category__in=categories).distinct()
        return queryset
