from django.views import generic
from django.urls import reverse_lazy

from home.models import ProductModel
from home.filters import ProductFilter
from .forms import ProductAddUpdateForm


class Dashboard(generic.TemplateView):
    template_name = "dashboard.html"


class ProductListView(generic.ListView):
    queryset = ProductModel.objects.all().order_by("-id")
    template_name = "products-list.html"
    context_object_name = "products"

    def get_queryset(self):
        filterd_queryset = ProductFilter(self.request.GET, queryset=self.queryset)
        return filterd_queryset


class ProductDetailView(generic.DetailView):
    model = ProductModel
    template_name = "product-detail.html"


class ProductAddView(generic.CreateView):
    model = ProductModel
    form_class = ProductAddUpdateForm
    template_name = "product-add.html"

    def get_success_url(self):
        extra_kwargs = {"slug": self.object.slug}
        return reverse_lazy("mod:product-detail", kwargs=extra_kwargs)


class ProductUpdateView(generic.UpdateView):
    model = ProductModel
    form_class = ProductAddUpdateForm
    template_name = "product-update.html"

    def get_success_url(self):
        extra_kwargs = {"slug": self.object.slug}
        return reverse_lazy("mod:product-detail", kwargs=extra_kwargs)


class ProductDeleteView(generic.DeleteView):
    model = ProductModel
