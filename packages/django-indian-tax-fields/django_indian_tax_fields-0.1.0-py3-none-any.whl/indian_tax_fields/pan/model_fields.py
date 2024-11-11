# Django imports
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

# Project imports
from indian_tax_fields.constants import PAN_MAX_LENGTH
from indian_tax_fields.pan import form_fields
from indian_tax_fields.pan.validators import pan_check


class PANField(CharField):
    default_validators = [pan_check]
    description = _("Permanent account number")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", PAN_MAX_LENGTH)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(**{"form_class": form_fields.PANField, **kwargs})
