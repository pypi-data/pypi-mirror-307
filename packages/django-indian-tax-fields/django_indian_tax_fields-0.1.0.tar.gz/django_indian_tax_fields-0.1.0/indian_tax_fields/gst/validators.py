# Python imports
import re

# Django imports
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Project imports
from indian_tax_fields.constants import GSTIN_REGEX


def gstin_check(value):
    """Checks a values validates as a GST Number.

    NOTE:
        A GST number is 15 digit alphanumeric.
        eg. 24 AAACB5343E 1 Z 7
        - First 2 digits are state code ranges 01-37
        - Next 10 digits is PAN Card number
            * First 3 are alphabets ranges from AAA-ZZZ
            * Next alphabet is either C,P,H,F,A,T,B,L,J,G,E
            * Next alphabet of Surname or Name
            * Next 4 digits range from 0001 to 9999
            * Next alphabetic check digit
        - 13th alphabets assigned based on the no. of reg. within a state
        - 14th alphabets will be Z by default
        - Last digit will be for check code. It may be an alphabet or a number.
    """
    pattern = re.compile(GSTIN_REGEX)
    if pattern.match(value) is None:
        raise ValidationError(_("Invalid GSTIN"), code="invalid_gst_number")
