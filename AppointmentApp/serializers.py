from django.utils import timezone
from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ("id", "doctor", "patient", "appointment_date", "reason", "prescription", "status", "duration_minutes", "created_at", "updated_at")
        read_only_fields = ("id", "patient", "created_at", "updated_at")

    def validate_appointment_date(self, value):
        if (self.instance is None or value != self.instance.appointment_date) and value <= timezone.now():
            raise serializers.ValidationError("Le rendez-vous doit être postérieur à maintenant.")
        return value
