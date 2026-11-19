from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from .validators import national_id_validator, phone_validator, validate_past_date


class User(AbstractUser):
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"

    def __str__(self):
        return self.name


class Doctor(User):
    license_number = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6)])
    phone = models.CharField(max_length=8, validators=[phone_validator])
    specialties = models.ManyToManyField(Specialty, blank=True, related_name="doctors")

    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"

    def __str__(self):
        return self.get_full_name() or self.username


class Patient(User):
    national_id = models.CharField(max_length=8, unique=True, validators=[national_id_validator])
    birth_date = models.DateField(validators=[validate_past_date])
    phone = models.CharField(max_length=8, validators=[phone_validator])

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return self.get_full_name() or self.username
