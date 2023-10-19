from django.urls import path
from .views import ConsultationPlanViewSet

urlpatterns = [
    path('consultationPlan', ConsultationPlanViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('consultationPlan/<str:pId>', ConsultationPlanViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('consultationPlan/<str:eId>/<str:prId>', ConsultationPlanViewSet.as_view({
        'get': 'retrieve_encounter',
        'put': 'update_encounter',
        'delete': 'destroy_encounter'
    }))
]
