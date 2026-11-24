from django import forms
from django.utils import timezone

from .models import Appointment


class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("doctor", "appointment_date", "reason")
        labels = {
            "doctor": "Médecin",
            "appointment_date": "Date et heure",
            "reason": "Motif de la consultation",
        }
        widgets = {
            "appointment_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "reason": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Expliquez brièvement le motif de votre demande..."},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["doctor"].queryset = self.fields["doctor"].queryset.order_by(
            "last_name", "first_name", "username"
        )

    def clean_appointment_date(self):
        value = self.cleaned_data["appointment_date"]
        if value <= timezone.now():
            raise forms.ValidationError("Choisissez une date et une heure futures.")
        return value

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get("doctor")
        appointment_date = cleaned_data.get("appointment_date")
        if doctor and appointment_date:
            conflict = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
            ).exists()
            if conflict:
                raise forms.ValidationError(
                    "Ce médecin a déjà un rendez-vous à cette date. Choisissez un autre créneau."
                )
        return cleaned_data
