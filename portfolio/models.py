"""Simple portfolio data model supporting investments in stocks."""
from django.db import models
import djmoney.models.fields as money_fields


class Stock(models.Model):
    """Represents a stock containing only basic attributes.

    A generic stock class (e.g. company share, equity fund, ... ) which stores only basic financial data of a
    tradable stock.

    :cvar isin: International Securities Identification Number (ISIN)
    :cvar wkn: German securities identification code named "Wertpapierkennnummer"
    :cvar name: name of stock
    """

    isin = models.CharField(max_length=12)
    wkn = models.CharField(max_length=6, blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        """Returns a nicely printable string representation of this Stock object.

        :return: a string representation of this stock
        """
        return self.name


class SharePrice(models.Model):
    """Represents the price of a share.

    The price of one share of a stock to a certian point in time.

    :cvar stock: stock which is the price related to
    :cvar date: date of the price
    :cvar price: price of one share
    """

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = money_fields.MoneyField(max_digits=12, decimal_places=6, default_currency='USD')

    def __str__(self):
        """Returns a nicely printable string representation of this SharePrice object.

        :return: a string representation of this share price.
        """
        return self.price


class Investment(models.Model):
    """Represents a financial investment in a stock.

    An investment refers to a stock in which the money was invested. It includes all order related information.

    :cvar stock: key of stock invested in
    :cvar date_of_order: date when stock was ordered
    :cvar order_price: order price of one share
    :cvar order_exchange_rate: exchange rate in force of order
    :cvar shares: amount of shares
    """

    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    date_of_order = models.DateField()
    order_price = money_fields.MoneyField(max_digits=11, decimal_places=2, default_currency='USD')
    order_exchange_rate = models.FloatField(blank=True, null=True)
    shares = models.FloatField()

    def __str__(self):
        """Returns a nicely printable string representation of this Investment object.

        :return: a string representation of this investment
        """
        return str(self.id)
