from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.views import generic, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest

from home.models import ImageModel, ProductModel
from . import forms


class ImageAddView(LoginRequiredMixin, StaffuserRequiredMixin, View):
    form_class = forms.ImageAddForm

    def get_success_url(self):
        print(self.request.POST.get("product"))
        kwargs = {"slug": get_object_or_404(ProductModel, id=self.request.POST.get("product")).slug}
        return reverse_lazy("mod:product-update", kwargs=kwargs)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        else:
            return HttpResponseBadRequest(f"form is not valid: {form.errors}")


class ImageDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, View):
    model = ImageModel

    def get_object(self):
        return get_object_or_404(self.model, id=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy("mod:product-update", kwargs={"slug": self.product_slug})

    def get(self, request, *args, **kwargs):
        model = self.get_object()
        self.product_slug = model.product.slug
        model.delete()
        return redirect(self.get_success_url())
