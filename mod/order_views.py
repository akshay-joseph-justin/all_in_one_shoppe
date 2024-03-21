from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from home.models import OrderModel


class OrderListView(LoginRequiredMixin, StaffuserRequiredMixin, generic.ListView):
    model = OrderModel
    template_name = "order-list.html"
    context_object_name = "objects"


class OrderDetailView(LoginRequiredMixin, StaffuserRequiredMixin, generic.DetailView):
    model = OrderModel
    template_name = "order-detail.html"
    context_object_name = "object"


class OrderDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, generic.DeleteView):
    model = OrderModel
    success_url = reverse_lazy("mod:order-list")
