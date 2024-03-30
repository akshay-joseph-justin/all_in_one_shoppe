from django import forms
from home import models


class ProductAddUpdateForm(forms.ModelForm):
    class Meta:
        model = models.ProductModel
        fields = "__all__"
        exclude = ("slug", "uuid")


class CategoryAddUpdateForm(forms.ModelForm):
    class Meta:
        model = models.CategoryModel
        fields = ("name",)


class ImageAddForm(forms.ModelForm):
    class Meta:
        model = models.ImageModel
        fields = "__all__"


class BannerForm(forms.ModelForm):
    class Meta:
        model = models.BannerModel
        fields = "__all__"


class PolicyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PolicyForm, self).__init__(*args, **kwargs)
        self.fields['text'].strip = False

    class Meta:
        model = models.PolicyModel
        fields = "__all__"
