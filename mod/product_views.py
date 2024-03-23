from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from home.models import ProductModel, CategoryModel, ImageModel
from home.filters import ProductFilter
from .forms import ProductAddUpdateForm


class ProductListView(LoginRequiredMixin, StaffuserRequiredMixin, generic.ListView):
    queryset = ProductModel.objects.all().order_by("-id")
    template_name = "products-list.html"
    context_object_name = "items"

    def get_queryset(self):
        filterd_queryset = ProductFilter(self.request.GET, queryset=self.queryset)
        return filterd_queryset.qs


class ProductDetailView(LoginRequiredMixin, StaffuserRequiredMixin, generic.DetailView):
    model = ProductModel
    template_name = "product-detail.html"


class ProductAddView(LoginRequiredMixin, StaffuserRequiredMixin, generic.CreateView):
    model = ProductModel
    form_class = ProductAddUpdateForm
    template_name = "product-add.html"

    def get_success_url(self):
        extra_kwargs = {"slug": self.object.slug}
        return reverse_lazy("mod:product-detail", kwargs=extra_kwargs)


class ProductUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, generic.UpdateView):
    model = ProductModel
    form_class = ProductAddUpdateForm
    template_name = "product-update.html"
    context_object_name = "item"

    def get_success_url(self):
        extra_kwargs = {"slug": self.object.slug}
        return reverse_lazy("mod:product-detail", kwargs=extra_kwargs)

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


class ProductDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, generic.DeleteView):
    model = ProductModel
    success_url = reverse_lazy("mod:product-list")
