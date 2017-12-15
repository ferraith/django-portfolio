from django.db import models
from djmoney.models.fields import MoneyField


class Stock(models.Model):
    isin = models.CharField(max_length=12)
    wkn = models.CharField(max_length=6, blank=True)
    name = models.CharField(max_length=200)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

    def __str__(self):
        return self.name


class Investment(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date_of_order = models.DateField()
    order_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    order_exchange_rate = models.FloatField(blank=True, null=True)
    shares = models.FloatField()

    def __str__(self):
        return str(self.id)
