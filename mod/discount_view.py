from django.views import generic
from django.urls import reverse_lazy

from home.models import DiscountModel
from .forms import DiscountAddUpdateForm


class DiscountListView(generic.ListView):
    model = DiscountModel
    template_name = "discount-list.html"
    context_object_name = "discounts"


class DiscountDetailView(generic.DetailView):
    model = DiscountModel
    template_name = "discount-detail.html"
    context_object_name = "discount"


class DiscountAddView(generic.CreateView):
    model = DiscountModel
    form_class = DiscountAddUpdateForm
    template_name = "discount-add.html"

    def get_success_url(self):
        extra_kwargs = {"id": self.object.id}
        return reverse_lazy("mod:discount-detail", kwargs=extra_kwargs)


class DiscountUpdateView(generic.UpdateView):
    model = DiscountModel
    form_class = DiscountAddUpdateForm
    template_name = "discount-update.html"

    def get_success_url(self):
        extra_kwargs = {"id": self.object.id}
        return reverse_lazy("mod:discount-detail", kwargs=extra_kwargs)


class DiscountDeleteView(generic.DeleteView):
    model = DiscountModel
