from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.views import generic, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect

from home.models import OrderProductModel, OrderModel


class OrderListView(LoginRequiredMixin, StaffuserRequiredMixin, generic.ListView):
    model = OrderModel
    template_name = "mod/order-list.html"
    context_object_name = "orders"


class OrderDetailView(LoginRequiredMixin, StaffuserRequiredMixin, View):
    model = OrderModel
    template_name = "mod/order-detail.html"
    context_object_name = "order"
    context_queryset_name = "products"
    extra_context_object_name = "total"

    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs.get("slug"))

    def get_queryset(self):
        return OrderProductModel.objects.filter(order=self.get_object())

    def get_extra_data(self):
        queryset = self.get_queryset()
        total = 0
        for order in queryset:
            total += order.quantity * order.product.price
        return total

    def get_extra_context_object_data(self):
        return {self.extra_context_object_name: self.get_extra_data()}

    def get_context_data(self):
        return {
            self.context_object_name: self.get_object(),
            self.context_queryset_name: self.get_queryset(),
            **self.get_extra_context_object_data()
        }

    def get(self, request, *args, **kwargs):
        print(self.get_context_data())
        return render(request, self.template_name, self.get_context_data())


class OrderUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, View):
    model = OrderModel

    def get_success_url(self):
        return reverse_lazy("mod:order-detail", kwargs={"slug": self.kwargs.get("slug")})

    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs.get("slug"))

    def get(self, request, *args, **kwargs):
        model = self.get_object()
        model.update(status="delivered")
        return redirect(self.get_success_url())
