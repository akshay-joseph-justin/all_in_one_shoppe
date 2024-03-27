from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views import generic
from django_filters.views import FilterView
from django.http import HttpResponseBadRequest
from . import models, filters, forms
import uuid


class IndexView(generic.RedirectView):
    pattern_name = "home:shop"


class ShopListView(FilterView, generic.ListView):
    queryset = models.ProductModel.objects.filter(available_stock__gt=0)
    template_name = "product-list.html"
    context_object_name = "items"
    filterset_class = filters.ProductFilter

    def get_queryset(self):
        queryset = self.queryset
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search) | Q(category__name__icontains=search))
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        queryset = self.filterset.qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"filter": self.filterset})
        return context


class ProductDetailView(View):
    model = models.ProductModel
    template_name = "product-detail.html"
    context_object_name = "item"

    def get_object(self):
        slug = self.kwargs.get("slug")
        queryset = get_object_or_404(self.model, slug=slug)
        return queryset

    def get_extra_context_data(self):
        product = self.get_object()
        Images = models.ImageModel.objects.filter(product=product)
        similar_products = self.model.objects.filter(name=product.name)
        print(similar_products)
        return {"images": Images, "sitems": similar_products}

    def get_context_data(self):
        queryset = self.get_object()
        extra_context_data = self.get_extra_context_data()
        context = {self.context_object_name: queryset, **extra_context_data}
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())


class CartListView(LoginRequiredMixin, generic.ListView):
    model = models.CartProductModel
    template_name = "cart.html"
    context_object_name = "items"

    def get_cart_object(self):
        return get_object_or_404(models.CartModel, user=self.request.user)

    def get_queryset(self):
        queryset = self.model.objects.filter(cart=self.get_cart_object())
        return queryset

    def get_extra_context_data(self, **kwargs):
        queryset = self.get_queryset()
        total = 0
        for query in queryset:
            total += query.quantity * query.product.price
        return {"total": total}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context_data())
        return context

    def create_cart_if_not_exists(self):
        cart = models.CartModel.objects.filter(user=self.request.user)
        if not cart:
            form_class = forms.CartAddForm
            form_data = {"user": self.request.user}
            form = form_class(form_data)
            if form.is_valid():
                form.save()
            else:
                return HttpResponseBadRequest(f"cart is not created {form.errors}")
    
    def get(self, *args, **kwargs):
        self.create_cart_if_not_exists()
        return super().get(*args, **kwargs)


class AddToCartView(LoginRequiredMixin, View):
    model = models.CartModel
    form_class = forms.CartAddForm

    def get_cart_object(self):
        return get_object_or_404(self.model, user=self.request.user)

    def get_cart_queryset(self):
        return models.CartProductModel.objects.filter(cart=self.get_cart_object())

    def product_exists_or_none(self, product, user):
        carts = self.get_cart_queryset()
        if carts:
            for cart in carts:
                if cart.product == product:
                    cart.quantity += 1
                    cart.save()
            return True
        else:
            return False

    def get_or_create_cart(self):
        cart = self.model.objects.filter(user=self.request.user)
        if not cart:
            form_data = {"user": self.request.user}
            form = self.form_class(form_data)
            if form.is_valid():
                form.save()
            else:
                return HttpResponseBadRequest(f"cart is not created {form.errors}")

    def get(self, request, slug):
        product = get_object_or_404(models.ProductModel, slug=slug)
        user = request.user
        self.get_or_create_cart()
        if not self.product_exists_or_none(product, user):
            quantity = request.GET.get("quantity") or 1
            cart = self.get_cart_object()
            form_class = forms.CartProductForm
            form_data = {"cart": cart, "product": product, "quantity": quantity}
            form = form_class(form_data)
            if form.is_valid():
                form.save()
                messages.success(request, "Item added to cart")
            else:
                messages.error(request, "item cannot be added to cart")

        return redirect(reverse_lazy("home:cart-list"))


class RemoveFromCart(LoginRequiredMixin, View):
    model = models.CartProductModel
    success_url = reverse_lazy("home:cart-list")

    def get_cart_object(self):
        return get_object_or_404(models.CartModel, user=self.request.user)

    def get_product_object(self):
        return get_object_or_404(models.ProductModel, slug=self.kwargs.get("slug"))

    def get_object(self):
        return get_object_or_404(self.model, cart=self.get_cart_object(), product=self.get_product_object())

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        queryset.delete()
        return redirect(self.success_url)


class PlaceOrderView(LoginRequiredMixin, View):
    model = models.OrderProductModel
    form_class = forms.OrderProductForm
    success_url = reverse_lazy("home:order-confirm")

    def create_order(self):
        if not self.get_order_object():
            form_class = forms.OrderAddForm
            form_data = {"user": self.request.user, "address": self.request.user.address, "status": "created"}
            form = form_class(form_data)
            if form.is_valid():
                form.save()
            else:
                return HttpResponseBadRequest(f"order cannot be created {form.errors}")

    def get_order_object(self):
        orders = models.OrderModel.objects.filter(user=self.request.user, status="created")
        for order in orders:
            if not self.model.objects.filter(order=order):
                return order
        return False

    def get_cart_queryset(self):
        cart = get_object_or_404(models.CartModel, user=self.request.user)
        return models.CartProductModel.objects.filter(cart=cart)

    def get(self, request, *args, **kwargs):
        self.create_order()
        order = self.get_order_object()
        carts = self.get_cart_queryset()
        for cart in carts:
            form_data = {"order": order, "product": cart.product, "quantity": cart.quantity}
            form = self.form_class(form_data)
            if form.is_valid():
                form.save()
            else:
                return HttpResponseBadRequest(f"order form error {form.errors}")

        return redirect(self.success_url)


class OrderConfirmationView(LoginRequiredMixin, View):
    model = models.OrderModel
    template_name = "order-confirm.html"
    context_object_name = "order"

    def get_queryset(self):
        orders = self.model.objects.filter(user=self.request.user, status="created")
        for order in orders:
            if models.OrderProductModel.objects.filter(order=order):
                return order

    def get_context_data(self):
        queryset = self.get_queryset()
        context_data = {self.context_object_name: queryset}
        return context_data

    def remove_from_cart(self, order):
        cart = get_object_or_404(models.CartModel, user=self.request.user)
        cart_products = models.CartProductModel.objects.filter(cart=cart)
        order_products = models.OrderProductModel.objects.filter(order=order)
        for order_product in order_products:
            for cart_product in cart_products:
                if order_product.product == cart_product.product:
                    cart_product.delete()

    def change_stock(self, order):
        queryset = models.OrderProductModel.objects.filter(order=order)
        for order_product in queryset:
            order_product.product.available_stock = int(order_product.product.available_stock) - 1
            order_product.product.save()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request):
        order = self.get_queryset()
        action = request.POST.get("action")
        if action == "cancel":
            order.delete()
            return redirect(reverse_lazy("home:cart-list"))

        if action == "confirm":
            form_data = {"user": request.user, "address": request.POST.get("address"), "status": request.POST.get("status")}
            form = forms.OrderAddForm(form_data, instance=order)
            if form.is_valid():
                form.save()
                self.remove_from_cart(order)
                self.change_stock(order)
                messages.success(request, "order placed successfully")
            else:
                messages.error(request, f"order cannot be placed {form.errors}")
            return redirect(reverse_lazy("home:order-detail", kwargs={"slug": order.slug}))


class OrderDetailView(LoginRequiredMixin, generic.ListView):
    model = models.OrderProductModel
    template_name = "order-detail.html"
    context_object_name = "orders"

    def get_queryset(self):
        order = get_object_or_404(models.OrderModel, slug=self.kwargs.get("slug"))
        return self.model.objects.filter(order=order)


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = models.OrderProductModel
    template_name = "order-list.html"
    context_object_name = "items"

    def get_queryset(self):
        return self.model.objects.filter(order__user=self.request.user)

    def create_if_not_exists(self):
        order = models.OrderModel.objects.filter(user=self.request.user)
        if not order:
            form_class = forms.OrderAddForm
            form_data = {"user": self.request.user, "address": self.request.user.address, "status": "created"}
            form = form_class(form_data)
            if form.is_valid():
                form.save()
            else:
                return HttpResponseBadRequest(f"order cannot be created {form.errors}")

    def get(self, *args, **kwargs):
        self.create_if_not_exists()
        return super().get(*args, **kwargs)
