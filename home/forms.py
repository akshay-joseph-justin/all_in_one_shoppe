from django import forms
from . import models


class CartAddForm(forms.ModelForm):
    class Meta:
        model = models.CartModel
        fields = "__all__"
        exclude = ("slug",)


class OrderAddForm(forms.ModelForm):
    class Meta:
        model = models.OrderModel
        fields = "__all__"
        exclude = ("uuid", "date")


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = models.OrderProductModel
        fields = "__all__"