import datetime

from django.core.exceptions import ValidationError


def validate_year(value: int) -> None:
    """Validate a year.
    Raises ValidationError if {value} > year now.
    """
    if value > datetime.date.today().year:
        raise ValidationError('Cannot add a future year')
