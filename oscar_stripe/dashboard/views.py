from django.views import generic

from .. import models


class StripeTransactionListView(generic.ListView):
    model = models.StripeTransaction
    template_name = 'stripe/stripe_transaction_list.html'
    context_object_name = 'stripe_transactions'


class StripeTransactionDetailView(generic.DetailView):
    model = models.StripeTransaction
    template_name = 'stripe/stripe_transaction_detail.html'
    context_object_name = 'stripe_transaction'

