"""Simple portfolio data model supporting investments in stocks."""
from django.db import models
import djmoney.models.fields as money_fields


class Portfolio(models.Model):
    """Represents a collection of investments.

    A portfolio is the top level entity of the portfolio data model which collects several investments.

    :cvar name: name of the portfolio
    """

    name = models.CharField(max_length=50, default='Untitled')

    def __str__(self):
        """Returns a nicely printable string representation of this Portfolio object.

        :return: a string representation of this portfolio
        """
        return self.name


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
    """Represents a financial investment.

    An investment spend on stocks consists of number of finance transactions for instance to buy it.

    :cvar portfolio: portfolio to which the investment belongs to
    :cvar stock: stock which is traded in this transaction
    """

    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT, default=0)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)

    def __str__(self):
        """Returns a nicely printable string representation of this Investment object.

        :return: a string representation of this investment
        """
        return str(self.id)


class Transaction(models.Model):
    """Represents a business agreement to exchange a stock for payment.

    This class represents a finance transaction to exchange a stock for payment e.g. to buy or to sell a certian
    amount of shares to a fixed price.

    :cvar investment: investment the transaction belongs to
    :cvar transaction_type: type of transaction
    :cvar transaction_date: date when transaction was executed
    :cvar share_price: price of one share at which transaction was executed
    :cvar exchange_rate: exchange rate in force of transaction
    :cvar volume: amount of shares
    """
    BUY = 'BUY'
    SALE = 'SAL'
    REINVESTMENT = 'REI'
    REDEMPTION = 'RED'
    DEPOT_FEE = 'DPF'
    TRANSACTION_TYPE = (
        ('BUY', 'Buy'),
        ('SAL', 'Sale'),
        ('REI', 'Reinvestment'),
        ('RED', 'Redemption'),
        ('DPF', 'Depot Fee'),
    )

    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE, default=BUY)
    transaction_date = models.DateField()
    share_price = models.ForeignKey(SharePrice, on_delete=models.PROTECT)
    exchange_rate = models.FloatField(blank=True, null=True)
    volume = models.FloatField()

    def __str__(self):
        """Returns a nicely printable string representation of this Transaction object.

        :return: a string representation of this transaction
        """
        return str(self.id)
