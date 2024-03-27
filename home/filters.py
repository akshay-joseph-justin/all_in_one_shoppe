import django_filters
from . import models
from django import forms

class ProductFilter(django_filters.FilterSet):
    size = django_filters.CharFilter(lookup_expr="icontains", widget=forms.TextInput(attrs={"placeholder": "M, L, XL", "class": "form-control"}))
    colour = django_filters.CharFilter(lookup_expr="icontains", widget=forms.TextInput(attrs={"placeholder": "choose your color", "class": "form-control"}))
    category = django_filters.ModelChoiceFilter(queryset=models.CategoryModel.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    class Meta:
        model = models.ProductModel
        fields = ("category", "size", "colour")
