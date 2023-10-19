from django.urls import path, re_path
from django.conf.urls import include


from . import views

urlpatterns = [
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('book_appointment_confirm/', views.book_appointment_confirm, name='book_appointment_confirm'),
    path('book_appointment_next_confirm/', views.book_appointment_next_confirm, name='book_appointment_next_confirm'),
    path('token_generated/', views.token_generated, name='token_generated'),
    path('search_patient/',views.search_patient,name='search_patient'),
    path('get_provider_free_slots/',views.getProviderFreeSlots,name='get_provider_free_slots')

]
