"""Admin interface of the portfolio app."""
from django.contrib import admin

from portfolio.models import Investment, Portfolio, SharePrice, Stock, Transaction


admin.site.register(Investment)
admin.site.register(Portfolio)
admin.site.register(SharePrice)
admin.site.register(Stock)
admin.site.register(Transaction)
