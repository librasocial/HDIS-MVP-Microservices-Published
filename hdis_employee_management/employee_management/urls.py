from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'employee-documents', EmployeeDocumentsViewSet)
router.register(r'employee-qualifications', EmployeeQualificationsViewSet)
router.register(r'providers', ProviderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
