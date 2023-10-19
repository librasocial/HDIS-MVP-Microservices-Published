from django.urls import path
from .views import PatientViewSet

urlpatterns = [
    path('patients', PatientViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('patients/<str:pId>', PatientViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('patients/uhid/<str:uhid>',PatientViewSet.as_view({
        'get':'search'
    }))
]
