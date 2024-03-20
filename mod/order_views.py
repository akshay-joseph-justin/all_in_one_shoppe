from django.views import generic

from home.models import OrderModel


class OrderListView(generic.ListView):
    model = OrderModel
    template_name = "order-list.html"
    context_object_name = "objects"


class OrderDetailView(generic.DetailView):
    model = OrderModel
    template_name = "order-detail.html"
    context_object_name = "object"


class OrderDeleteView(generic.DeleteView):
    model = OrderModel
