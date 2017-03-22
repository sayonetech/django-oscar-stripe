import json

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .base_models import RequestResponse


@python_2_unicode_compatible
class StripeTransaction(RequestResponse):
    description = models.CharField(_("Description of the Transaction"),
                                   help_text="Description of the transaction", max_length=128)
    transaction_type = models.CharField(_("Transaction Type"), help_text='The type of transaction',
                                        max_length=12)
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text='Amount',
                                 null=True, blank=True)
    currency = models.CharField(_("Currency"), help_text='currency', max_length=3)
    transaction_date = models.DateTimeField(_('Transaction Date'), auto_now_add=True)

    def _get_transaction_id(self):
        return json.loads(self.raw_response)['id']

    def _get_transaction_status(self):
        return 'succeeded' == json.loads(self.raw_response)['status']

    stripe_transaction_id = property(_get_transaction_id)
    stripe_transaction_status = property(_get_transaction_status)

    class Meta:
        abstract = False
        ordering = ('-date_created',)
        verbose_name = _('Stripe Transaction')
        verbose_name_plural = _('Stripe Transactions')

