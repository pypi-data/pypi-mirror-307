# Django Indian Tax Fields

>This repository is a fork of the original repository [django-gst-field](https://github.com/jinchuuriki91/django-gst-field). This fork is created to maintain the code and extend the original scope.

# Contents

A Django library which provides model and form fields for `Goods and Services Tax` and `Permanent Account Number`

Includes:

- `GSTField`, form and model field
- `PANField`, form and model field

## Installation

```
pip install django-indian-tax-fields
```

### Basic usage

Add `indian_tax_fields` to the list of the installed apps in Django `settings.py` file:

```python
INSTALLED_APPS = [
    ...
    'indian_tax_fields',
    ...
]
```

### Model usage

```python
from django.conf import settings
from django.db.models import ForeignKey, CASCADE, Model

from indian_tax_fields.gst.model_fields import GSTField
from indian_tax_fields.pan.model_fields import PANField

class Tax(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    gstin = GSTField()
    pan = PANField()
```
