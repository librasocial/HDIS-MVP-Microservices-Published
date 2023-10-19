from django.urls import path, re_path
from django.conf.urls import include


from . import views

urlpatterns = [
    path("opd_consultation/", views.opd_consultation, name='opd_consultation')
]
