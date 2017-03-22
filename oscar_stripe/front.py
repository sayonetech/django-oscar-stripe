from . import gateway
from oscar.apps.payment import exceptions


def simple_payment(order_number, amount, currency, bankcard, billing_address=None, description=None):
    """
    make payment using card.
    """
    return _submit_payment_details(gateway.make_payment, order_number, amount, currency,
                                   bankcard, billing_address, description)


def _submit_payment_details(gateway_fn, order_number, amount, currency, bankcard, billing_address, description):
    """
    call the function from gateway module for making payment.
    """
    address_fields = {}
    if billing_address:

        address_fields.update(
            {
                'first_name': billing_address.get('first_name'),
                'last_name': billing_address.get('last_name'),
                'street': billing_address.get('line1'),
                'city': billing_address.get('line4'),
                'state': billing_address.get('state'),
                'zip': billing_address.get('postcode').strip(' ')
            }
        )
    stripe_payment = gateway_fn(order_number,
                                bankcard.number,
                                bankcard.ccv,
                                bankcard.expiry_date.month,
                                bankcard.expiry_date.year,
                                amount,
                                currency,
                                description,
                                **address_fields)

    if not stripe_payment.stripe_transaction_status:
        raise exceptions.UnableToTakePayment(stripe_payment.raw_response)

    return stripe_payment
