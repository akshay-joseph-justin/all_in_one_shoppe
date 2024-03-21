from django import forms
from . import models

class CartAddForm(forms.ModelForm):
    class Meta:
        model = models.CartModel
        fields = "__all__"