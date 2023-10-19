from django.urls import path
from .views import PatientViewSet

urlpatterns = [
    path('patients', PatientViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('person/<str:pId>', PatientViewSet.as_view({
        'get': 'retrievePerson',
        'put': 'updatePerson',
        'delete': 'destroyPerson'
    })),
    path('patients/<str:pId>', PatientViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('patients/uhid/<str:uhid>',PatientViewSet.as_view({
        'get':'search'
    })),
    path('patients/facilitySearch/<str:lfpId>',PatientViewSet.as_view({
        'get':'searchByLocalID'
    })),
    path('patients/search/', PatientViewSet.as_view({
        'post': 'fetch',
    })),
]
