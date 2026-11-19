from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from AppointmentApp.models import Appointment

from .models import Doctor, Patient, Specialty


class AccountModelTests(TestCase):
    def test_business_identifiers_and_specialties(self):
        doctor = Doctor.objects.create_user(username="doctor", password="secret", license_number="ABC123", phone="12345678")
        patient = Patient.objects.create_user(
            username="patient", password="secret", national_id="12345678",
            birth_date=date(1990, 1, 1), phone="87654321",
        )
        doctor.specialties.add(Specialty.objects.create(name="Cardiologie"))
        self.assertEqual(doctor.pk, doctor.user_ptr_id)
        self.assertEqual(patient.pk, patient.user_ptr_id)
        self.assertEqual(doctor.specialties.count(), 1)

    def test_birth_date_and_phone_are_validated(self):
        patient = Patient(
            username="patient", national_id="12345678",
            birth_date=date.today() + timedelta(days=1), phone="123",
        )
        with self.assertRaises(ValidationError):
            patient.full_clean()


class AppointmentModelTests(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(username="doctor", password="secret", license_number="ABC123", phone="12345678")
        self.patient = Patient.objects.create_user(
            username="patient", password="secret", national_id="12345678",
            birth_date=date(1990, 1, 1), phone="87654321",
        )

    def test_past_appointment_is_rejected_on_creation(self):
        appointment = Appointment(
            doctor=self.doctor, patient=self.patient,
            appointment_date=timezone.now() - timedelta(hours=1), reason="Consultation",
        )
        with self.assertRaises(ValidationError):
            appointment.full_clean()

    def test_doctor_cannot_have_duplicate_slot(self):
        appointment_date = timezone.now() + timedelta(days=1)
        Appointment.objects.create(
            doctor=self.doctor, patient=self.patient,
            appointment_date=appointment_date, reason="Consultation",
        )
        duplicate = Appointment(
            doctor=self.doctor, patient=self.patient,
            appointment_date=appointment_date, reason="Contrôle",
        )
        with self.assertRaises(ValidationError):
            duplicate.validate_constraints()
