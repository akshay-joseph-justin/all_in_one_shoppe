from django.views import generic
from braces.views import StaffuserRequiredMixin, LoginRequiredMixin


class RedirectView(generic.RedirectView):
    pattern_name = "mod:order-list"
