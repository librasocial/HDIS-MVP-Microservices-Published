from .views import *
from django.urls import include, path
from rest_framework.routers import DefaultRouter

# Register URLs for default CRUD operations
router = DefaultRouter()
router.register(r'service-types', ServiceTypeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'component-services', ComponentServiceViewSet)
router.register(r'service-prices', ServicePriceViewSet)
router.register(r'service-discounts', ServiceDiscountViewSet)
router.register(r'service-taxes', ServiceTaxViewSet)

urlpatterns = [
    path('services/facility/<uuid:fid>/', ServiceViewSet.as_view({
            'get': 'list_by_facility',
        })),
    path('services/provider/uhpn/<str:uhpn>/', ServiceViewSet.as_view({
            'get': 'list_by_provider_uhnp',
        })),
    path('', include(router.urls)),    
] 