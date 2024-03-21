from braces.views import StaffuserRequiredMixin, LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from home.models import CartModel


class CartListView(LoginRequiredMixin, StaffuserRequiredMixin, generic.ListView):
    model = CartModel
    template_name = "cart-list.html"
    context_object_name = "reviews"


class CartDetailView(LoginRequiredMixin, StaffuserRequiredMixin, generic.DetailView):
    model = CartModel
    template_name = "cart-detail.html"


class CartDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, generic.DeleteView):
    model = CartModel
    success_url = reverse_lazy("mod:cart-list")
