from django.urls import path, re_path
from django.conf.urls import include


from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('get_or_create_patient/', views.get_or_create_patient, name='get_or_create_patient'),
    #path('abha_mobile_otp_verification/', views.abha_mobile_otp_verification, name='abha_mobile_otp_verification')
]
