"""Admin interface of the portfolio app."""
from django.contrib import admin

from portfolio.models import Asset, Bond, Fund, Investment, Portfolio, SharePrice, Stock, Transaction


admin.site.register(Asset)
admin.site.register(Bond)
admin.site.register(Fund)
admin.site.register(Investment)
admin.site.register(Portfolio)
admin.site.register(SharePrice)
admin.site.register(Stock)
admin.site.register(Transaction)
