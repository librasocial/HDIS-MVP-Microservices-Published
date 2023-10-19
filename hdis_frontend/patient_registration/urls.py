from django.urls import path, re_path
from django.conf.urls import include


from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    #path('abha_mobile_otp_verification/', views.abha_mobile_otp_verification, name='abha_mobile_otp_verification')
]
