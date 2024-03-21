from django.views import generic
from braces.views import StaffuserRequiredMixin, LoginRequiredMixin


class RedirectToDashboardView(generic.RedirectView):
    pattern_name = "mod:product-list"


class Dashboard(LoginRequiredMixin, StaffuserRequiredMixin, generic.TemplateView):
    template_name = "Dashboard.html"
