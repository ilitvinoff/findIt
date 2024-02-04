import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def phoneNumberValidator(phone):
    if phone is not None:
        try:
            parsed_phone = phonenumbers.parse(phone)
            if not phonenumbers.is_valid_number(parsed_phone):
                raise ValidationError([_('Phone number is incorrect.')], code='incorrect')
        except phonenumbers.NumberParseException:
            raise ValidationError([_('Phone number is incorrect.')], code='incorrect')
