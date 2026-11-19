from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Doctor, Patient, Specialty, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email")


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("username", "license_number", "phone", "email")
    search_fields = ("username", "first_name", "last_name", "license_number")
    filter_horizontal = ("specialties",)

    def get_readonly_fields(self, request, obj=None):
        return ("license_number",) if obj else ()


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("username", "national_id", "birth_date", "phone", "email")
    search_fields = ("username", "first_name", "last_name", "national_id")

    def get_readonly_fields(self, request, obj=None):
        return ("national_id",) if obj else ()
