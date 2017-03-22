from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class RequestResponse(models.Model):
    raw_request = models.TextField(_("Raw Request"), help_text=_('The raw request'),max_length=750)
    raw_response = models.TextField(_("Raw Response"), help_text=_('The raw response'), max_length=750)
    date_created = models.DateTimeField(_("Date Created"), help_text=_('The DateTime when request was made.'),
                                        auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-date_created',)

    def __str__(self):
        return self.raw_request

