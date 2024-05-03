"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from facility_management.views import *
from rest_framework.routers import DefaultRouter

# Register URLs for default CRUD operations
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'packagetypes', PackageTypeViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'facilitytypes', FacilityTypeViewSet)
router.register(r'facilities', FacilityViewSet)

urlpatterns = [
    path('facilitytypes/<int:facility_type_code>/roles', FacilityTypeViewSet.as_view({
        'get': 'list_roles_for_facility_type',
    }), name = "list_roles_for_facility_type"),
    path('facilities/applications/', FacilityViewSet.as_view({
        'post': 'create_from_application',
    }), name = "create_from_application"),
    path('', include(router.urls)),
]