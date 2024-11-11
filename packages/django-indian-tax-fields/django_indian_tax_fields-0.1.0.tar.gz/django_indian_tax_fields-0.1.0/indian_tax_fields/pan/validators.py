# Python imports
import re

# Django imports
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Project imports
from indian_tax_fields.constants import PAN_REGEX


def pan_check(value):
    """Checks a values validates as a PAN Number.

    NOTE:
        A PAN number is 10 digit alphanumeric.
        eg. AAA C B 5343 E
        - First 3 are alphabets ranges from AAA-ZZZ
        - Next alphabet is either C,P,H,F,A,T,B,L,J,G,E
        - Next alphabet of Surname or Name
        - Next 4 digits range from 0001 to 9999
        - Next alphabetic check digit
    """
    pattern = re.compile(PAN_REGEX)
    if pattern.match(value) is None:
        raise ValidationError(_("Invalid PAN"), code="invalid_pan_number")
