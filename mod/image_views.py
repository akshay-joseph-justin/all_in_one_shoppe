from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.views import generic, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest

from home.models import ImageModel, ProductModel
from . import forms


class ImageAddView(LoginRequiredMixin, StaffuserRequiredMixin, View):
    form_class = forms.ImageAddForm

    def get_success_url(self, product):
        kwargs = {"slug": product.slug}
        return reverse_lazy("mod:product-update", kwargs=kwargs)

    def post(self, request):
        slug = request.POST.get("slug")
        product = get_object_or_404(ProductModel, slug=slug)
        form_data = {"product": product, "image": request.FILES.get("image")}
        print(form_data)
        form = self.form_class(form_data)
        print(request.FILES.get("image"))
        if form.is_valid():
            form.save()
            return self.get_success_url(product)
        else:
            return HttpResponseBadRequest(f"form is not valid: {form.errors}")


class ImageDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, generic.DeleteView):
    model = ImageModel

    def get_success_url(self):
        queryset = self.get_object()
        return reverse_lazy("mod:product-update", kwargs={"slug": queryset.product.slug})
