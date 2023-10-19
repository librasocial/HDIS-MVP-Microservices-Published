from django.urls import path, re_path
from django.conf.urls import include


from . import views

urlpatterns = [
    path('hospitals_clinics/', views.hospitals_clinics, name='hospitals_clinics'),
    path('diagnostic_labs/', views.diagnostic_labs, name='diagnostic_labs'),
    path('pharmacies/', views.pharmacies, name='pharmacies'),
    path('register_facility/', views.register_facility, name='register_facility'),
    path('select_microservices/', views.select_microservices, name='select_microservices'),

]
