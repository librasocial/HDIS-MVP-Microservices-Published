from django.urls import path, re_path
from django.conf.urls import include


from . import views

urlpatterns = [
    path('search_patient_visit/', views.search_patient, name='search_patient_visit'),
    path('check_in/', views.checkin, name='check_in'),

]
