# Django imports
from django.forms.fields import CharField
from django.utils.translation import gettext_lazy as _

# Project imports
from indian_tax_fields.gst.validators import gstin_check


class GSTField(CharField):
    default_error_messages = {"invalid": _("Enter a valid GST number.")}
    default_validators = [gstin_check]

    def __init__(self, **kwargs):
        super().__init__(strip=True, **kwargs)
