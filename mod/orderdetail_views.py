from django.views import generic

from home.models import OrderDetailModel


class OrderDetailListView(generic.ListView):
    model = OrderDetailModel
    template_name = "order-detail-list.html"
    context_object_name = "orders"


class OrderDetailDetailView(generic.DetailView):
    model = OrderDetailModel
    template_name = "order-detail-detail.html"


class OrderDetailDeleteView(generic.DeleteView):
    model = OrderDetailModel
