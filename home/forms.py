from django import forms
from . import models


class CartAddForm(forms.ModelForm):
    class Meta:
        model = models.CartModel
        fields = "__all__"


class OrderAddForm(forms.ModelForm):
    class Meta:
        model = models.OrderModel
        fields = "__all__"
        exclude = ("uuid", "date")