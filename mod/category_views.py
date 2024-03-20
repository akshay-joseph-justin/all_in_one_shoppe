from django.views import generic
from django.urls import reverse_lazy

from home.models import CategoryModel
from .forms import CategoryAddUpdateForm


class CategoryListView(generic.ListView):
    model = CategoryModel
    template_name = "category-list.html"
    context_object_name = "categories"


class CategoryDetailView(generic.DetailView):
    model = CategoryModel
    template_name = "category-detail.html"


class CategoryAddView(generic.CreateView):
    model = CategoryModel
    form_class = CategoryAddUpdateForm
    template_name = "category-add.html"

    def get_success_url(self):
        extra_kwargs = {"slug": self.object.slug}
        return reverse_lazy("mod:category-detail", kwargs=extra_kwargs)



class CategoryUpdateView(generic.UpdateView):
    model = CategoryModel
    form_class = CategoryAddUpdateForm
    template_name = "category-update.html"

    def get_success_url(self):
        extra_kwargs = {"slug": self.object.slug}
        return reverse_lazy("mod:category-detail", kwargs=extra_kwargs)


class CategoryDeleteView(generic.DeleteView):
    model = CategoryModel
