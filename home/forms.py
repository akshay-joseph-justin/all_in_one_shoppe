from django import forms
from . import models


class CartAddForm(forms.ModelForm):
    class Meta:
        model = models.CartModel
        fields = "__all__"
        exclude = ("slug", )


class CartProductForm(forms.ModelForm):
    class Meta:
        model = models.CartProductModel
        fields = "__all__"


class OrderAddForm(forms.ModelForm):
    class Meta:
        model = models.OrderModel
        fields = "__all__"
        exclude = ("uuid", "date", "slug")


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = models.OrderProductModel
        fields = "__all__"