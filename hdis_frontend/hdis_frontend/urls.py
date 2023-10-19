"""hdis_frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from access_frontend.views import login,dashboard
from access_frontend.views import logout,home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('appointment_booking/', include('appointment_booking.urls')),
    #path('consultation/', include('consultation.urls')),
    #path('op_billing/', include('op_billing.urls')),
    path('doctor_administration/', include('doctor_administration.urls')),
    path('patient_registration/', include('patient_registration.urls')),
    path('access_frontend/', include('access_frontend.urls')),
    path('visit_management/', include('visit_management.urls')),
    path('consultation/', include('consultation.urls')),
    path('login/', login),
    path('logout/', logout),
    path('dashboard/', dashboard),
    path('', home)



    #path('queue_management/', include('queue_management.urls')),
]
