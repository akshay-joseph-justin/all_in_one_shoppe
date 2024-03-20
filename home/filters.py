import django_filters
from . import models


class ProductFilter(django_filters.Filter):
    class Meta:
        model = models.ProductModel
        fields = ("category", "price", "size", "color")
