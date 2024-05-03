from .views import *
from django.urls import path

urlpatterns = [
    path('', ConsultationPlanViewSet.as_view({
        #'get': 'list',    #For troubleshooting only
        'post': 'create',
    }), name='consultationplan-list'),
    path('clinical-notes/<str:cnid>', ConsultationPlanViewSet.as_view({
        'get': 'retrieve_clinical_note',
    }), name='consultationplan-detail'),
    path('encounter/<str:eid>', ConsultationPlanViewSet.as_view({
        'get': 'retrieve_for_encounter',
    }), name='consultationplan-encounterdetail'),
    path('order-sets', OrderSetViewSet.as_view({
        #'get': 'list',    #For troubleshooting only
        'post': 'create',
    }), name='orderset-list'),
    path('order-sets/orders', OrderSetViewSet.as_view({
        'delete': 'destroy_order_set_order',
    }), name='orderset-order-list'),
    path('order-sets/provider/<str:pid>', OrderSetViewSet.as_view({
        'get': 'retrieve_for_provider',
    }), name='orderset-providerdetail'),
    path('order-sets/<str:osid>', OrderSetViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    }), name='orderset-detail'),
]
