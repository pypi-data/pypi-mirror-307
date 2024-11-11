# Django imports
from django.forms.fields import CharField
from django.utils.translation import gettext_lazy as _

# Project imports
from indian_tax_fields.pan.validators import pan_check


class PANField(CharField):
    default_error_messages = {"invalid": _("Enter a valid PAN number.")}
    default_validators = [pan_check]

    def __init__(self, **kwargs):
        super().__init__(strip=True, **kwargs)
