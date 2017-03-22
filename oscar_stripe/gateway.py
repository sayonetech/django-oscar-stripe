import json

import stripe

from django.utils.timezone import now
from django.conf import settings
from .models import StripeTransaction
from .exceptions import OscarStripeException, StripeAPIException


def make_payment(order_number, card_number, ccv, expiry_month, expiry_year,
                 amount, currency, description=None, **kwargs):
    return _submit_payment_details(order_number, card_number, ccv, expiry_month, expiry_year,
                                   amount, currency, description, **kwargs)


def _submit_payment_details(order_number, card_number, ccv, expiry_month, expiry_year, amount, currency,
                            description, **kwargs):
    params = {
        'DESCRIPTION': str(order_number) if description is None else description,
        'AMOUNT':amount,
        'CURRENCY':currency,
        # Bankcard
        'CARDNUMBER': card_number,
        'CCV': ccv,
        'EXPMONTH': expiry_month,
        'EXPYEAR': expiry_year,
        'FIRSTNAME': kwargs.get('first_name', ''),
        'LASTNAME': kwargs.get('last_name', ''),
        'STREET': kwargs.get('street', ''),
        'CITY': kwargs.get('city', ''),
        'STATE': kwargs.get('state', ''),
        'ZIP': kwargs.get('zip', ''),
        'BILLTOCOUNTRY': kwargs.get('countrycode', ''),
        'EMAIL': kwargs.get('user_email', ''),
        'PHONENUM': kwargs.get('billing_phone_number', ''),
    }

    return _transaction(params)


def _transaction(params):
    if 'AMOUNT' and 'CARDNUMBER' and 'CCV' and 'EXPMONTH' and 'EXPYEAR' and 'CURRENCY' not in params:
        raise OscarStripeException('AMOUNT, CARDNUMBER, EXPMONTH, EXPYEAR, CVV should be specified for payment.')

    for setting_attribute in ('STRIPE_API_KEY',):
        if not hasattr(settings, setting_attribute):
            raise OscarStripeException('You must define %s in settings'%setting_attribute)

    if len(str(params['CCV'])) not in [3,4]:
        raise OscarStripeException('The length of ccv should be 3 or 4')

    if len(str(params['CURRENCY'])) != 3:
        raise OscarStripeException('Invalid Currency.')

    if int(params['EXPYEAR']) < now().year:
        raise OscarStripeException('Invalid Expiry Year')

    if int(params['EXPYEAR']) == now().year and params['EXPMONTH'] < now().month:
        raise OscarStripeException(' Invalid expiry month')

    return _make_charge(params) # Actual transaction takes place here.


def _make_charge(params):
    """
    Stripe charge created here.
    """
    stripe.api_key = settings.STRIPE_API_KEY
    stripe_token_id = _create_stripe_token(params['CARDNUMBER'], params['CCV'], params['EXPMONTH'], params['EXPYEAR'])
    amount = _convert_to_integer(params['AMOUNT'])

    try:
        response = stripe.Charge.create(amount=amount,
                                        currency=params['CURRENCY'],
                                        source=stripe_token_id,
                                        description=params['DESCRIPTION'])
    except Exception as e:
        raise StripeTransaction('Stripe API error in making charge: ' + str(e))

    return StripeTransaction.objects.create(
        raw_request=json.dumps(params),
        raw_response=json.dumps(response),
        amount=amount,
        currency=params['CURRENCY'],
        transaction_type='Card Payment',
        description=params['DESCRIPTION'],
    )


def _convert_to_integer(amount):
    """
    amount converted to integer(to cents) for stripe payment.
    """
    try:
        amount = int(float(amount) * 100)  # convert to cents since decimal amount not accepted .
    except Exception as e:
        raise OscarStripeException('Invalid amount provided: ' + str(e))

    return amount


def _create_stripe_token(card_number, cvv, exp_month, exp_year):
    """
    stripe token creation for payment done here.
    """
    try:
        stripe_token = stripe.Token.create(
            card={'number': card_number, 'exp_month': exp_month, 'exp_year': exp_year, 'cvc': cvv}
        )
    except Exception as e:
        raise StripeAPIException('Stripe API error in creating token: ' + str(e))

    return stripe_token.id
