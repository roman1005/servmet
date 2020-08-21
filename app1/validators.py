from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validateRGB(value):
    if value <  0 or value > 255:
        raise ValidationError(
            _('%(value)s is out of RGB range (0...255)'),
            params={'value': value},
        )