from django.views import generic
from django.urls import reverse_lazy

from home.models import ReviewModel


class ReviewListView(generic.ListView):
    model = ReviewModel
    template_name = "review-list.html"
    context_object_name = "reviews"


class ReviewDetailView(generic.DetailView):
    model = ReviewModel
    template_name = "review-detail.html"


class ReviewDeleteView(generic.DeleteView):
    model = ReviewModel
