from rest_framework.routers import DefaultRouter

from .views import DoctorViewSet, PatientViewSet, SpecialtyViewSet

router = DefaultRouter()
router.register("specialties", SpecialtyViewSet)
router.register("doctors", DoctorViewSet)
router.register("patients", PatientViewSet)
urlpatterns = router.urls
