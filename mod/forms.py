from django import forms
from home import models


class ProductAddUpdateForm(forms.ModelForm):
    class Meta:
        model = models.ProductModel
        fields = "__all__"
        exclude = ("slug", "uuid")


class CategoryAddUpdateForm(forms.ModelForm):
    class Meta:
        model = models.CartModel
        fields = "__all__"
