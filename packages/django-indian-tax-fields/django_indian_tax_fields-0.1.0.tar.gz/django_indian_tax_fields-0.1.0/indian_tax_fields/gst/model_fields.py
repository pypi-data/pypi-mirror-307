# Django imports
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

# Project imports
from indian_tax_fields.constants import GSTIN_MAX_LENGTH
from indian_tax_fields.gst import form_fields
from indian_tax_fields.gst.validators import gstin_check


class GSTField(CharField):
    default_validators = [gstin_check]
    description = _("Goods and Services Tax")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", GSTIN_MAX_LENGTH)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(**{"form_class": form_fields.GSTField, **kwargs})
