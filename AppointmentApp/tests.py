from datetime import date, timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from AccountApp.models import Doctor, Patient

from .models import Appointment


class AppointmentApiTests(APITestCase):
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

    def test_duplicate_slot_returns_400(self):
        self.client.force_login(self.patient)
        payload = {
            "doctor": self.doctor.pk,
            "appointment_date": (timezone.now() + timedelta(days=3)).isoformat(),
            "reason": "Consultation",
        }
        self.assertEqual(self.client.post("/api/appointments/", payload, format="json").status_code, 201)
        self.assertEqual(self.client.post("/api/appointments/", payload, format="json").status_code, 400)

    def test_doctor_cannot_create_appointment(self):
        self.client.force_login(self.doctor)
        response = self.client.post(
            "/api/appointments/",
            {
                "doctor": self.doctor.pk,
                "appointment_date": (timezone.now() + timedelta(days=3)).isoformat(),
                "reason": "Consultation",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)


class FrontendPageTests(APITestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            username="doctor", password="secret", license_number="ABC123", phone="12345678",
        )
        self.patient = Patient.objects.create_user(
            username="patient", password="secret", national_id="12345678",
            birth_date=date(1990, 1, 1), phone="87654321",
        )

    def test_public_pages_render(self):
        for url in ("/", "/apropos/", "/accounts/login/"):
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_appointment_page_requires_login(self):
        response = self.client.get("/api/prendre-rendez-vous/")
        self.assertRedirects(response, "/accounts/login/?next=/api/prendre-rendez-vous/")

    def test_patient_can_book_from_form(self):
        self.client.force_login(self.patient)
        appointment_date = (timezone.localtime() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M")
        response = self.client.post(
            "/api/prendre-rendez-vous/",
            {"doctor": self.doctor.pk, "appointment_date": appointment_date, "reason": "Consultation"},
        )
        self.assertRedirects(response, "/api/rendez-vous-confirme/")
        self.assertEqual(Appointment.objects.get().patient_id, self.patient.pk)
