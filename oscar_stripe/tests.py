from datetime import datetime, timedelta

from django.test import TestCase
from django_oscar_stripe.exceptions import OscarStripeException, StripeAPIException
from django_oscar_stripe.gateway import _transaction, convert_to_integer


class TestGateway(TestCase):
    """
    Tests performing in gateway module.
    """
    def test_parameter_requirement(self):
        """
        if all the required parameters are present.
        """
        params = {
        'DESCRIPTION': 'test description',
        'CURRENCY':'USD',
        # Bankcard
        'CARDNUMBER': '4242424242424242',
        'CCV': 123,
        'EXPMONTH': 12,
        'EXPYEAR': (datetime.now() + timedelta(days=2*365)).year,
        'FIRSTNAME': 'test first name',
        'LASTNAME': 'test last name',
        'STREET': 'test street',
        'CITY': 'test city',
        'STATE': 'test state',
        'ZIP': 'test zip',
        'BILLTOCOUNTRY': 'test billtocountry',
        'EMAIL': 'test email',
        'PHONENUM': '12345678',
        }
        self.assertRaises(OscarStripeException, _transaction, params)

    def test_valid_amount(self):
        """
        Check if OscarStripeException raised when amount entered is invalid.
        """
        amount = '10A2321.23'
        self.assertRaisesMessage(OscarStripeException,convert_to_integer, amount)



