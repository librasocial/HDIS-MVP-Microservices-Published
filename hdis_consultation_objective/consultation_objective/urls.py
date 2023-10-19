from django.urls import path
from .views import ConsultationObjectivetViewSet

urlpatterns = [
    path('consultationObjective', ConsultationObjectivetViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('consultationObjective/<str:pId>', ConsultationObjectivetViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('consultationObjective/<str:eId>/<str:prId>', ConsultationObjectivetViewSet.as_view({
        'get': 'retrieve_encounter',
        'put': 'update_encounter',
        'delete': 'destroy_encounter'
    }))
]
