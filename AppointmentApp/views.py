from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from AccountApp.models import Patient

from .forms import AppointmentRequestForm
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
            raise ValidationError(
                {"appointment_date": "Ce médecin a déjà un rendez-vous à cette date."}
            ) from exc


@login_required
def request_appointment(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        patient = None

    if patient is None:
        if request.user.is_staff:
            return redirect("admin:index")
        messages.error(
            request,
            "Vous devez disposer d'un profil patient pour prendre un rendez-vous.",
        )
        return redirect("accueil")

    form = AppointmentRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        appointment = form.save(commit=False)
        appointment.patient = patient
        try:
            with transaction.atomic():
                appointment.full_clean()
                appointment.save()
        except IntegrityError:
            form.add_error(
                "appointment_date",
                "Ce médecin a déjà un rendez-vous à cette date. Choisissez un autre créneau.",
            )
            return render(
                request,
                "AppointmentApp/request_appointment.html",
                {"form": form},
            )
        messages.success(
            request,
            "Votre demande de rendez-vous a été enregistrée avec succès.",
        )
        return redirect("appointment_success")

    return render(
        request,
        "AppointmentApp/request_appointment.html",
        {"form": form},
    )


@login_required
def appointment_success(request):
    return render(request, "AppointmentApp/appointment_success.html")
