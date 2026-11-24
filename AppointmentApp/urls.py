from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AppointmentViewSet, appointment_success, request_appointment

router = DefaultRouter()
router.register("appointments", AppointmentViewSet)
urlpatterns = [
    path("prendre-rendez-vous/", request_appointment, name="request_appointment"),
    path("rendez-vous-confirme/", appointment_success, name="appointment_success"),
]
urlpatterns += router.urls
