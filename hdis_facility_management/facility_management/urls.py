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
from facility_management.views import FacilityViewSet,MemberViewSet

urlpatterns = [
    path('facility/', FacilityViewSet.as_view({
        'post': 'create',
        'get':'list',
    })),
    path('facilitytype/', FacilityViewSet.as_view({
        'get':'facilityType',
    })),
    path('facility/<str:fId>', FacilityViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('facilityuser/<str:Upk>', MemberViewSet.as_view({
        'get':'retrieveUser',
        'put':'updateUser',
    
    
    })),
    path('facilityuser/', MemberViewSet.as_view({
        'post':'addUser',
    
    
    
    })),
   path('facilityusertypes/', FacilityViewSet.as_view({
        'get':'listUserType',
    
    
    
    }))
]