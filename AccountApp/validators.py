from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


phone_validator = RegexValidator(
    regex=r"^\d{8}$",
    message="Le numéro de téléphone doit contenir exactement 8 chiffres.",
)


national_id_validator = RegexValidator(
    regex=r"^\d{8}$",
    message="Le numéro CIN doit contenir exactement 8 chiffres.",
)


def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError("La date de naissance doit être antérieure à aujourd'hui.")
