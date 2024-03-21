from django.views import generic
from braces.views import StaffuserRequiredMixin, LoginRequiredMixin


class Dashboard(LoginRequiredMixin, StaffuserRequiredMixin, generic.TemplateView):
    template_name = "Dashboard.html"
