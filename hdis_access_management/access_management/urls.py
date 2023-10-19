from django.urls import path
from . import views
from .views import OpenHDISTokenObtainPairView,AccessViewSet
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns = [

path('token/', OpenHDISTokenObtainPairView.as_view(), name='token_obtain_pair'),
#path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
path('register/', AccessViewSet.as_view({'post': 'Register',}), name='register_user'),
path('setpassword/', AccessViewSet.as_view({'post': 'ChangePass',}), name='change_pass'),
path('check_access/',AccessViewSet.as_view({'post': 'CheckAccess',}), name='check_access'),
path('update_user/',AccessViewSet.as_view({'post': 'UpdateUser',}), name='update_user'),
path('add_user/',AccessViewSet.as_view({'post': 'AddUser',}), name='add_user'),

] 