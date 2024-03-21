from django.views import View
from django.views import generic
from django_filters.views import FilterView
from django.db.models import Q
from braces.views import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from . import models, filters, forms


class IndexView(generic.RedirectView):
    pattern_name = "home:shop"


class ShopListView(FilterView, generic.ListView):
    queryset = models.ProductModel.objects.filter(available_stock__gt=0)
    context_object_name = "items"
    filterset_class = filters.ProductFilter

    def get_queryset(self):
        queryset = self.get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query) |
                Q(category__icontains=query)
            )
        return queryset


class ProductDetailView(generic.DetailView):
    model = models.ProductModel
    template_name = "product-detail.html"


class ShopListImageView(generic.ListView):
    model = models.ImageModel
    template_name = "shop.html"


class ProductImageView(generic.DetailView):
    model = models.ImageModel
    template_name = "product-detail.html"


class CartListView(LoginRequiredMixin, generic.ListView):
    model = models.CartModel
    template_name = "cart-list.html"
    context_object_name = "items"

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset


class CartAddView(View):

    model = models.CartModel
    form_class = forms.CartAddForm

    def exists_or_none(self, product, user):
        return self.model.objects.filter(user=user, product=product)

    def post(self, request, slug):
        product = get_object_or_404(models.ProductModel, slug=slug)
        user = request.user
        form_data = {
            "user": user,
            "product": product,
        }
        form = self.form_class(data=form_data)
        if form.is_valid():
            form.save()
            messages.success(request, "Item added to cart")
        else:
            messages.error(request, "item cannot be added to cart")