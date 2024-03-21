from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.views import generic

from home.models import ReviewModel


class ReviewListView(LoginRequiredMixin, StaffuserRequiredMixin, generic.ListView):
    model = ReviewModel
    template_name = "review-list.html"
    context_object_name = "reviews"


class ReviewDetailView(LoginRequiredMixin, StaffuserRequiredMixin, generic.DetailView):
    model = ReviewModel
    template_name = "review-detail.html"


class ReviewDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, generic.DeleteView):
    model = ReviewModel
