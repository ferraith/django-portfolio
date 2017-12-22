"""Simple portfolio data model supporting investments in stocks."""
from django.db import models
from django.utils.translation import ugettext_lazy as _
import djmoney.models.fields as money_fields


class Portfolio(models.Model):
    """Represents a collection of investments.

    A portfolio is the top level entity of the portfolio data model which collects several investments.

    :cvar name: name of the portfolio
    """

    name = models.CharField(_('Name'), max_length=50, default=_('Untitled'))

    def __str__(self):
        """Returns a nicely printable string representation of this Portfolio object.

        :return: a string representation of this portfolio
        """
        return self.name

    class Meta:
        verbose_name = _('Portfolio')
        verbose_name_plural = _('Portfolios')


class Asset(models.Model):
    """Represents an economic resource.

    The Asset class is the root of all financial instruments. It holds attributes which are common for all instruments
    e.g. an issuer.

    :cvar name: name of asset
    :cvar isin: International securities identification number (ISIN)
    :cvar issuer: Legal entity that develops, registers and sells the asset
    :cvar cusip: North American securities identification code (CUSIP)
    :cvar wkn: German securities identification code (Wertpapierkennnummer)
    :cvar valor: Switzerland securities identification code (VALOR)
    """

    name = models.CharField(_('Name'), max_length=200)
    isin = models.CharField(_('ISIN'), max_length=12)
    issuer = models.CharField(_('Issuer'), max_length=50)
    cusip = models.CharField(_('CUSIP'), max_length=9, blank=True, default='')
    wkn = models.CharField(_('WKN'), max_length=6, blank=True, default='')
    valor = models.PositiveIntegerField(_('VALOR'), blank=True, null=True)

    def __str__(self):
        """Returns a nicely printable string representation of an Asset object.

        :return: a string representation of the asset
        """
        return self.name

    class Meta:
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')


class Fund(Asset):
    """Represents an investment fund collectively invests in financial instruments.

    An investment fund is a supply of capital belonging to numerous investors used to collectively purchase securities
    like stocks or bonds.

    :cvar ter: Total expense ratio
    """

    ter = models.DecimalField(_('TER'), max_digits=3, decimal_places=2)

    class Meta:
        verbose_name = _('Fund')
        verbose_name_plural = _('Funds')


class Bond(Asset):
    """Represents a bond (e.g. government bond).

    A bond which can be issued by certian organizations like governments, financial institutions or companies.

    :cvar funds: collection of bond funds investigating in this bond
    """

    funds = models.ManyToManyField(Fund, verbose_name=_('Funds'), blank=True)

    class Meta:
        verbose_name = _('Bond')
        verbose_name_plural = _('Bonds')


class Stock(Asset):
    """Represents a stock (e.g. company share).

    A stock which is typically issued by a company operating in a specific sector.

    :cvar sector: economic sector of issuer
    :cvar funds: collection of stock funds investigating in this stock
    """

    sector = models.CharField(_('Sector'), max_length=200)
    funds = models.ManyToManyField(Fund, verbose_name=_('Funds'), blank=True)

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')


class SharePrice(models.Model):
    """Represents the price of a share.

    The price of one share of an asset to a certian point in time.

    :cvar asset: asset which is the price related to
    :cvar date: date of the price
    :cvar price: price of one share
    """

    asset = models.ForeignKey(Asset, verbose_name=_('Asset'), on_delete=models.CASCADE)
    date = models.DateTimeField(_('Date'))
    price = money_fields.MoneyField(_('Price'), max_digits=12, decimal_places=6, default_currency='USD')

    def __str__(self):
        """Returns a nicely printable string representation of this SharePrice object.

        :return: a string representation of this share price.
        """
        return "{} ({})".format(self.date, self.price)

    class Meta:
        verbose_name = _('Share price')
        verbose_name_plural = _('Share prices')


class Investment(models.Model):
    """Represents a financial investment.

    An investment spend on an asset consists of number of finance transactions for instance to buy it.

    :cvar portfolio: portfolio to which the investment belongs to
    :cvar asset: an economic resource which is invested in
    """

    portfolio = models.ForeignKey(Portfolio, verbose_name=_('Portfolio'), on_delete=models.PROTECT, default=0)
    asset = models.ForeignKey(Asset, verbose_name=_('Asset'), on_delete=models.PROTECT)

    def __str__(self):
        """Returns a nicely printable string representation of this Investment object.

        :return: a string representation of this investment
        """
        return '{} ({})'.format(self.asset.name, self.id)

    class Meta:
        verbose_name = _('Investment')
        verbose_name_plural = _('Investments')


class TransactionType:
    """Collection of valid transaction types."""

    BUY = 'BUY'
    SALE = 'SAL'
    REINVESTMENT = 'REI'
    REDEMPTION = 'RED'
    DEPOT_FEE = 'DPF'


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

    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        _('Transaction type'),
        max_length=3,
        choices=(
            (TransactionType.BUY, _('Buy')),
            (TransactionType.SALE, _('Sale')),
            (TransactionType.REINVESTMENT, _('Reinvestment')),
            (TransactionType.REDEMPTION, _('Redemption')),
            (TransactionType.DEPOT_FEE, _('Depot Fee')),
        ),
        default=TransactionType.BUY
    )
    transaction_date = models.DateField(_('Transaction date'))
    share_price = models.ForeignKey(SharePrice, verbose_name=_('Share price'), on_delete=models.PROTECT)
    exchange_rate = models.DecimalField(_('Exchange rate'), max_digits=12, decimal_places=6, blank=True, null=True)
    volume = models.DecimalField(_('Volume'), max_digits=15, decimal_places=6)

    def __str__(self):
        """Returns a nicely printable string representation of this Transaction object.

        :return: a string representation of this transaction
        """
        return '{} ({})'.format(self.get_transaction_type_display(), self.investment.asset.name)

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
