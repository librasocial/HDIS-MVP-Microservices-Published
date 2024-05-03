from .views import *
from django.urls import include, path
from rest_framework.routers import DefaultRouter

# Register URLs for default CRUD operations
router = DefaultRouter()
router.register(r'sources-of-payment', SourceOfPaymentViewSet)
router.register(r'bills', BillViewSet)

urlpatterns = [
    path('bills/<str:bid>/items/', BillViewSet.as_view({
            'post': 'create_bill_items', 'get': 'retrieve_bill_with_items'
        })),
    path('bills/items/<str:ipk>/', BillViewSet.as_view({
            'get': 'retrieve_bill_item', 'delete': 'destroy_bill_item', 
            'put': 'update_bill_item', 'patch': 'partial_update_bill_item'
        })),
    path('', include(router.urls)),
]
