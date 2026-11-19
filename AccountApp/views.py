from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Doctor, Patient, Specialty
from .serializers import DoctorSerializer, PatientSerializer, SpecialtySerializer


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.prefetch_related("specialties").all()
    serializer_class = DoctorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
