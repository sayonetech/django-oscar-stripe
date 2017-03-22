
class OscarStripeException(Exception):
    """
    Exception raised if exception arises in gateway module.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class StripeAPIException(Exception):
    """
    Exception raised in case of API failure of stripe.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message