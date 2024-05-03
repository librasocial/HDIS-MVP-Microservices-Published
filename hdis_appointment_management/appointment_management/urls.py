from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Register URLs for default CRUD operations
router = DefaultRouter()
router.register(r'resource-schedules', ResourceScheduleViewSet, basename='resourceschedule')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'resource-unavailability', ResourceUnavailabilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
