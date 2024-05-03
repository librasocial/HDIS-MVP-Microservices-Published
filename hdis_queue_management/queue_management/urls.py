from .views import *
from django.urls import path

urlpatterns = [
    path('queues/', QueueViewSet.as_view({
        'post': 'join_queue',
    }), name='queue-post'),
    path('queues/search', QueueViewSet.as_view({
        'get': 'search',
    }), name='queue-search'),
]