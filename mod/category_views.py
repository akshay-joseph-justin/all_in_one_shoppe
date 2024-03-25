from braces.views import StaffuserRequiredMixin, LoginRequiredMixin
from django.views import generic, View
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404

from home.models import CategoryModel
from .forms import CategoryAddUpdateForm


class CategoryListView(LoginRequiredMixin, StaffuserRequiredMixin, generic.ListView):
    model = CategoryModel
    template_name = "category-list.html"
    context_object_name = "categories"


class CategoryAddView(LoginRequiredMixin, StaffuserRequiredMixin, generic.CreateView):
    model = CategoryModel
    form_class = CategoryAddUpdateForm
    template_name = "category-add.html"
    success_url = reverse_lazy("mod:category-list")


class CategoryUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, generic.UpdateView):
    model = CategoryModel
    form_class = CategoryAddUpdateForm
    template_name = "category-update.html"
    context_object_name = "object"
    success_url = reverse_lazy("mod:category-list")


class CategoryDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, View):
    model = CategoryModel
    success_url = reverse_lazy("mod:category-list")

    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs.get("slug"))

    def get_success_url(self):
        return self.success_url

    def get(self, request, *args, **kwargs):
        model = self.get_object()
        model.delete()
        return redirect(self.get_success_url())
