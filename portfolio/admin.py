"""Admin interface of the portfolio app."""
from django.contrib import admin

from portfolio.models import Investment


admin.site.register(Investment)
