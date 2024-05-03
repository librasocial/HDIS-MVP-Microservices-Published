from django.urls import include, path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'memberships', FacilityMembershipViewSet)  #TODO: Decide whether to retain for Admin
                
urlpatterns = [
    path('', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('registration/', MemberViewSet.as_view({'post': 'register_members'}), name='register_members'),
    path('members/username/<str:username>', MemberViewSet.as_view({
        'get': 'retrieve_member_by_username', 
        'put': 'update_member_by_username', 
        'delete': 'deactivate_user_by_username'
    }), name='member_by_username'),
    path('members/username/<str:username>/password/', MemberViewSet.as_view({'put': 'update_password'}), name='update_password'),
    path('members/<str:mid>/membership/', MemberViewSet.as_view({'get': 'get_membership_for_member'}), name='get_membership_for_member'),
    path('members/facility/<str:fid>', MemberViewSet.as_view({'get': 'list_members_of_facility'}), name='list_members_of_facility'),
    path('members/<str:mid>/facility/<str:fid>', MemberViewSet.as_view({'get': 'get_facility_roles_for_member'}), name='get_facility_roles_for_member'),
]
