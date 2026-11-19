from datetime import date, timedelta

from django.test import TestCase
from django.utils import timezone

from AccountApp.models import Doctor, Patient

from .models import Appointment


class AppointmentApiTests(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            username="doctor",
            password="secret",
            license_number="ABC123",
            phone="12345678",
        )
        self.patient = Patient.objects.create_user(
            username="patient",
            password="secret",
            national_id="12345678",
            birth_date=date(1990, 1, 1),
            phone="87654321",
        )

    def test_api_creation_links_current_patient(self):
        self.client.force_login(self.patient)
        response = self.client.post(
            "/api/appointments/",
            {
                "doctor": self.doctor.pk,
                "patient": 999999,
                "appointment_date": (
                    timezone.now() + timedelta(days=3)
                ).isoformat(),
                "reason": "Demande via API",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        appointment = Appointment.objects.get()
        self.assertEqual(appointment.patient_id, self.patient.pk)
