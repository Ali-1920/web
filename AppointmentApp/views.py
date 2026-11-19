from django.db import IntegrityError, transaction
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from AccountApp.models import Patient

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related("doctor", "patient").all()
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        try:
            patient = self.request.user.patient
        except Patient.DoesNotExist as exc:
            raise PermissionDenied(
                "Seul un patient peut créer un rendez-vous."
            ) from exc
        try:
            with transaction.atomic():
                serializer.save(patient=patient)
        except IntegrityError as exc:
            raise PermissionDenied(
                "Ce médecin a déjà un rendez-vous à cette date."
            ) from exc
