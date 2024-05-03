from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Register URLs for default CRUD operations
router = DefaultRouter()
router.register(r'visits', VisitViewSet, basename='visit')
router.register(r'episodes', EpisodeViewSet, basename='episode')

urlpatterns = [    
    path('', include(router.urls)),
] 