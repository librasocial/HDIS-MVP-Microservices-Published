from django.urls import path, re_path
from django.conf.urls import include


from . import views

urlpatterns = [

    path('login/',views.login,name='login'),
    path('register_facility/', views.register_facility, name='register_facility'),
    path('select_microservices/', views.select_microservices, name='select_microservices'),
    path('setpassword/(?P<token>[\w\W\s\S]*)(?P<next>[\w\W\s\S]*)', views.setpassword, name='setpassword'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('nurse_profile/', views.nurse_profile, name='nurse_profile'),
    path('facilityusers/', views.facilityusers, name='facilityusers'),   
    path('edituser/', views.edituser, name='edituser'),
    path('getuserdetails/<str:uId>', views.getuserdetails, name='getuserdetails'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('adduser/', views.adduser, name='adduser'),
    path('superadmin/', views.superadmin, name='superadmin'),
    path('bulkupload/', views.bulkupload, name='bulkupload'),
    path('front_desk_home/',views.front_desk_home,name='front_desk_home'),
    path('search_patient/',views.search_patient,name='search_patient'),
    path('search_patient_mobile/',views.search_patient_mobile,name='search_patient_mobile'),
    path('search_patient_demo/',views.search_patient_demo,name='search_patient_demo'),

    path('', views.home, name='home')
]
