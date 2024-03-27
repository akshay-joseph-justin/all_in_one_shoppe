import django_filters
from . import models


class ProductFilter(django_filters.FilterSet):
    size = django_filters.CharFilter(lookup_expr="icontains")
    colour = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.ProductModel
        fields = ("category", "size", "colour")
