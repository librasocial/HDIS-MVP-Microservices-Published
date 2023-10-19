from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [

path('get_providers/', views.getProviders, name='get_providers'),
path('get_provider_schedule/', views.getProviderSchedule, name='get_provider_schedule'),
path('get_provider_appointment/',views.getAppointmentsforProvider,name='get_provider_appointment'),
path('get_provider_appointment_slots/', views.getProviderAppointmentSlots, name='get_provider_appointment_slots'),
path('create_appointment/', views.createAppointment, name='create_appointment'),
path('get_patient_appointment/', views.getAppointmentsforPatient, name='get_patient_appointment'),




] 