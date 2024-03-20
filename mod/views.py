from django.views import generic


class Dashboard(generic.TemplateView):
    template_name = "Dashboard.html"