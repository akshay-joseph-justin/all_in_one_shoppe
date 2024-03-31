from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from home import models
from .forms import BannerForm, PolicyForm


class RedirectView(generic.RedirectView):
    pattern_name = "mod:order-list"


class BannerListView(generic.ListView):
    model = models.BannerModel
    template_name = "banner-list.html"
    context_object_name = "banners"


class BannerAddView(generic.CreateView):
    model = models.BannerModel
    form_class = BannerForm
    template_name = "banner-add.html"
    success_url = reverse_lazy("mod:banner-list")


class BannerDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, View):
    model = models.BannerModel
    success_url = reverse_lazy("mod:banner-list")

    def get_object(self):
        return get_object_or_404(self.model, id=self.kwargs.get("pk"))

    def get_success_url(self):
        return self.success_url

    def get(self, request, *args, **kwargs):
        model = self.get_object()
        model.delete()
        return redirect(self.get_success_url())


class PolicyView(generic.ListView):
    model = models.PolicyModel
    template_name = "policy.html"
    context_object_name = "policy"


class PolicyUpdateView(generic.UpdateView):
    model = models.PolicyModel
    form_class = PolicyForm
    template_name = "policy-update.html"
    context_object_name = "policy"
    success_url = reverse_lazy("mod:policy")
