from django.urls import path
from .views import DoctorViewSet

urlpatterns = [
    path('doctors', DoctorViewSet.as_view({
        'post': 'create',
    })),
    path('doctors/', DoctorViewSet.as_view({
        'get': 'list',
    })),
    path('doctors_detail/<str:dId>', DoctorViewSet.as_view({
        'get': 'retrieve',
        'post': 'update',
        'delete': 'destroy'
    })),
    path('doctor_field_check/<str:fId>', DoctorViewSet.as_view({
        'get': 'retrieveFields',
        'put': 'updateFields'
    })),
    path('doctor_provider_details/<str:dId>', DoctorViewSet.as_view({
        'get': 'getprovider',
    })),
    path('provider/<str:dId>', DoctorViewSet.as_view({
        'get': 'retrieveProvider',
    }))
]
