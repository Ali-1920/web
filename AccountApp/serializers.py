from rest_framework import serializers

from .models import Doctor, Patient, Specialty


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("id", "name")


class DoctorSerializer(serializers.ModelSerializer):
    specialties = SpecialtySerializer(many=True, read_only=True)
    specialty_ids = serializers.PrimaryKeyRelatedField(
        source="specialties", queryset=Specialty.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:
        model = Doctor
        fields = ("id", "username", "first_name", "last_name", "email", "license_number", "phone", "specialties", "specialty_ids")
        read_only_fields = ("id", "username")


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "username", "first_name", "last_name", "email", "national_id", "birth_date", "phone")
        read_only_fields = ("id", "username")
