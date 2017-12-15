"""Views representing the user interface of the portfolio app."""
from django.views import generic

from portfolio.models import Investment


class IndexView(generic.ListView):
    template_name = 'portfolio/index.html'
    context_object_name = 'investment_list'

    def get_queryset(self):
        return Investment.objects.all()
