from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views import generic
from django_filters.views import FilterView

from . import models, filters, forms


class IndexView(generic.RedirectView):
    pattern_name = "home:shop"


class ShopListView(FilterView, generic.ListView):
    queryset = models.ProductModel.objects.filter(available_stock__gt=0)
    template_name = "product-list.html"
    context_object_name = "items"
    filterset_class = filters.ProductFilter

    def get_queryset(self):
        queryset = self.queryset
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query))
        return queryset


class ProductDetailView(generic.DetailView):
    model = models.ProductModel
    template_name = "product-detail.html"


class CartListView(LoginRequiredMixin, generic.ListView):
    model = models.CartModel
    template_name = "cart-list.html"
    context_object_name = "items"

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset


class AddToCartView(LoginRequiredMixin, View):
    model = models.CartModel
    form_class = forms.CartAddForm

    def exists_or_none(self, product, user):
        cart = self.model.objects.filter(user=user, product=product)
        if cart:
            cart.quantity += 1
        else:
            return None

    def post(self, request, slug):
        product = get_object_or_404(models.ProductModel, slug=slug)
        user = request.user
        if self.exists_or_none(product, user) is not None:
            quantity = request.POST.get("quantity") or 1
            form_data = {"user": user, "product": product, "quantity": quantity}
            form = self.form_class(data=form_data)
            if form.is_valid():
                form.save()
                messages.success(request, "Item added to cart")
            else:
                messages.error(request, "item cannot be added to cart")

        return redirect(request.get_full_path())


class RemoveFromCart(LoginRequiredMixin, generic.DeleteView):
    model = models.CartModel

    def get_success_url(self):
        return self.request.get_full_path()


class PlaceOrderView(LoginRequiredMixin, View):
    model = models.OrderModel
    form_class = forms.OrderAddForm

    def post(self, request, slug):
        product = get_object_or_404(models.ProductModel, slug=slug)
        quantity = request.POST.get("quantity") or 1
        form_data = {"user": request.user, "product": product, "quantity": quantity, "address": request.user.address,
                     "status": "ordered", }
        form = self.form_class(data=form_data)
        if form.is_valid():
            form.save()
            messages.success(request, "order listed successfully")
        else:
            messages.error(request, "order cannot be listed")
        return redirect(reverse_lazy("home:order-conform"))


class OrderConfirmationView(LoginRequiredMixin, View):
    model = models.OrderModel
    template_name = "order-confirm.html"
    context_object_name = "order"

    def get_queryset(self, **kwargs):
        return self.model.objects.get(**kwargs)

    def get_context_data(self):
        queryset = self.get_queryset(user=self.request.user)
        context_data = {self.context_object_name: queryset, }
        return context_data

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, response):
        uuid = request.POST.get("uuid")
        order = self.get_queryset(uuid=uuid)
        if not response:
            order.delete()
            return redirect(reverse_lazy("home:shop"))

        if response:
            form = forms.OrderAddForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                messages.success(request, "order placed successfully")
            else:
                messages.error(request, "order cannot be placed")
            return redirect(reverse_lazy("home:order-detail", kwargs={uuid: order.uuid}))


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.OrderModel
    template_name = "order-detail.html"
    context_object_name = "order"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
