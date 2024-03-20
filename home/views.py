from django.views import View
from django.views import generic

from . import models
from . import filters


class IndexView(generic.RedirectView):
    pattern_name = "home:shop"


class ShopView(generic.ListView):
    queryset = models.ProductModel.objects.filter(available_stock__gt=0)
    template_name = "index.html"
    context_object_name = "items"

    def get_queryset(self):
        filter = filters.ProductFilter(self.request.GET, queryset=self.queryset)
        return filter