"""Admin interface of the portfolio app."""
from django.contrib import admin

from portfolio.models import Investment, SharePrice, Stock


admin.site.register(Investment)
admin.site.register(SharePrice)
admin.site.register(Stock)
