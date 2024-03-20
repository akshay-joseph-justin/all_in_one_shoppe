from django.views import generic
from django.urls import reverse_lazy

from home.models import ImageModel
from .forms import ImageAddUpdateForm


class ImageListView(generic.ListView):
    model = ImageModel
    template_name = "image-list.html"
    context_object_name = "images"


class ImageDetailView(generic.DetailView):
    model = ImageModel
    template_name = "image-detail.html"


class ImageAddView(generic.CreateView):
    model = ImageModel
    form_class = ImageAddUpdateForm
    template_name = "image-add.html"

    def get_success_url(self):
        extra_kwargs = {"id": self.object.id}
        return reverse_lazy("mod:image-detail", kwargs=extra_kwargs)


class ImageUpdateView(generic.UpdateView):
    model = ImageModel
    form_class = ImageAddUpdateForm
    template_name = "image-update.html"

    def get_success_url(self):
        extra_kwargs = {"id": self.object.id}
        return reverse_lazy("mod:image-detail", kwargs=extra_kwargs)


class ImageDeleteView(generic.DeleteView):
    model = ImageModel