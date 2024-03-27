from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import generic, View
from django.urls import reverse_lazy

from home.models import ProductModel, CategoryModel, ImageModel
from home.filters import ProductFilter
from .forms import ProductAddUpdateForm


class ProductListView(LoginRequiredMixin, StaffuserRequiredMixin, generic.ListView):
    queryset = ProductModel.objects.all().order_by("-id")
    template_name = "mod/products-list.html"
    context_object_name = "items"

    def get_queryset(self):
        filterd_queryset = ProductFilter(self.request.GET, queryset=self.queryset)
        return filterd_queryset.qs


class ProductDetailView(LoginRequiredMixin, StaffuserRequiredMixin, generic.DetailView):
    model = ProductModel
    template_name = "mod/product-detail.html"


class ProductAddView(LoginRequiredMixin, StaffuserRequiredMixin, generic.CreateView):
    model = ProductModel
    form_class = ProductAddUpdateForm
    template_name = "product-add.html"
    success_url = reverse_lazy("mod:product-list")

    def get_extra_context_data(self):
        queryset = CategoryModel.objects.all()
        return {"categories": queryset}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context_data())
        return context


class ProductUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, generic.UpdateView):
    model = ProductModel
    form_class = ProductAddUpdateForm
    template_name = "product-update.html"
    context_object_name = "item"
    success_url = reverse_lazy("mod:product-list")

    def get_extra_context_data(self):
        categories = CategoryModel.objects.all()
        product = self.get_object()
        images = ImageModel.objects.filter(product=product)
        context = {"categories": categories, "images": images}
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context_data())
        return context


class ProductDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, View):
    model = ProductModel
    success_url = reverse_lazy("mod:product-list")

    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs.get("slug"))

    def get_success_url(self):
        return self.success_url

    def get(self, request, *args, **kwargs):
        model = self.get_object()
        model.delete()
        return redirect(self.get_success_url())
