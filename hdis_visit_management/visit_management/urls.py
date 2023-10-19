from django.urls import path
from . import views
from .views import VisitViewSet
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [

    path('visit_check_in/', VisitViewSet.as_view({
            'post': 'checkin',
    })),
    path('episode/<str:epId>', VisitViewSet.as_view({
            'get': 'retrieveEpisode',
    }))
] 