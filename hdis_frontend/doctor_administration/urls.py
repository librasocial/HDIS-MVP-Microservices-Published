from django.urls import path, re_path
from django.conf.urls import include


from . import views

urlpatterns = [
    path('doctor_list/', views.doctor_list, name='doctor_list'),
    path('doctor_details/<str:dId>',views.doctor_details,name='doctor_details'),
    path('doctor_details_update/<str:dId>',views.doctor_details_update,name='doctor_details_update'),
    path('facility_field_check/<str:fId>',views.facility_field_check,name='facility_field_check'),
    path('facility_field_check_update/<str:fId>',views.facility_field_check_update,name='facility_field_check_update'),
]
