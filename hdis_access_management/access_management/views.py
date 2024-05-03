from .serializers import *
from datetime import datetime, timedelta
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, Application
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope


class IsSuperuserPermission(permissions.BasePermission):
    """ Custom Permission permitting actions only for Superusers. """

    def has_permission(self, request, view):
        print("User:", request.user)
        print("Superuser:", request.user.is_superuser)
        if request.user and request.user.is_superuser:
            return True
        else:
            return False


class IsTrustedClientPermission(permissions.BasePermission):
    """ Custom Permission permitting actions only for trusted clients authenticated via OAuth2 Client credentials Grant Type. """

    def has_permission(self, request, view):
        if request.auth is None:    #Ensure that an OAuth2 Access Token is present
            print("IsTrustedCClientPermission: Access denied due to missing Access Token.") #Debug TODO: Log error details
            return False
        
        # Grant access when authentication has occurred via OAuth2 Client Credentials Grant Type.
        requestor = request.user
        grant_type = request.auth.application.get_authorization_grant_type_display()
        if grant_type == 'Client credentials':
            if requestor is None:    #If there is no User associated with the Client Credential...
                request.user = request.auth.application.user  #... treat the user linked to the Application (if any) as the requestor
            return True


class IsFacilityAdminPermission(permissions.BasePermission):
    """ Custom Permission permitting actions only for Administrators of the Facility ID passed as a View parameter. """

    def has_permission(self, request, view):
        if request.auth is None:    #Ensure that an OAuth2 Access Token is present
            print("IsFacilityAdminPermission: Access denied due to missing Access Token.") #Debug TODO: Log error details
            return False
        
        # Process requests from an Authenticated User holding a valid Access Token.
        requestor = request.user
        if requestor:
            mid = requestor.id   #Get ID of Requesting User
        else:
            print("IsFacilityAdminPermission: Access denied to Anonymous User.") #Debug TODO: Log error details
            return False
        fid = view.kwargs.get('fid')    #Get Facility ID passed to the View
        if not fid:
            print("IsFacilityAdminPermission: Access denied as no Facility ID was passed to the View.") #Debug TODO: Log error details
            return False   #Deny access if Member ID or Facility ID parameter has not been passed

        # Check Membership
        membership = FacilityMembership.objects.filter(member_id=mid, facility_id=fid).prefetch_related("group")
        member_role_names = [ member_role.group.name for member_role in membership ]
        print("Member Roles:", member_role_names) #Debug
        return "Admin" in member_role_names


class MemberViewSet(viewsets.ModelViewSet):
    """ Defines CRUD operations on the Member entity managed only by the Superuser and Facility Admin Roles. """

    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    # By default, allow standard ModelViewSet actions only for valid OAuth2 Tokens held by Superusers and Internal Services.
    permission_classes = [TokenHasReadWriteScope]#, IsTrustedClientPermission | IsSuperuserPermission]    #TODO: Resolve issue with method-level overrides

    def get_permissions(self):
        # Among the standard ModelViewSet actions, set up custom permissions for 'retrieve'
        # Note that permissions for non-standard ViewSet actions are customized using the @action decorator.
        if self.action == 'retrieve':
             return [TokenHasReadWriteScope()]    #Authorize any valid OAuth Token holder
        else:
            return super().get_permissions()
    
    
    def register_members(self, request):
        """
        Register one or more Members of a particular, existing Facility in specified Roles. For use only by Superusers or 
        Facility Admins of that Facility. Also returns an Access Token that the Facility Admin can immediately log in with.
        """

        request_data = request.data
        error_body = {
            "type": request.build_absolute_uri("/errors/missing-request-data"),
            "title": "Mandatory attribute not provided.",
            "detail": "An expected, mandatory attribute '{}' was not found in the request body."
        }

        facility_id = None
        try:
            facility_id = request_data['facility_id']
            members_to_create = request_data['members']
        except KeyError as ke:
            error_body["detail"] = error_body["detail"].format(ke.args[0])
            return Response(error_body, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Implement Facility ID validation for guaranteed data integrity even in case of an invalid request?

        if not members_to_create:    #If "members" is an empty list...
            error_body["title"] = "List of Members to be created is empty."
            error_body["detail"] = "At least one Member must be created in a request."
            return Response(error_body, status=status.HTTP_400_BAD_REQUEST)
        
        headers = None
        response_body = []
        for member_to_create in members_to_create:    #TODO: Wrap each Member creation in a transaction?
            try:    #Catch & handle any exceptions while processing individual members without aborting processing of other members 
                new_member = roles_for_member = role_error = None
                member_response = {}
                member_errors = {"input_username": member_to_create.get("username", None)}    #Dev Note: Used to prepend username to errors encountered while creating each member
                serializer = self.get_serializer(data=member_to_create)
                roles_for_member = serializer.initial_data.pop('roles')    #Remove "roles" attribute from serializer data for separate processing
                if serializer.is_valid(raise_exception=False):    #Fail silently in case valiadtion of a particular member fails
                    serializer.validated_data["is_staff"] = member_to_create.get('is_staff', False)  #TODO: Should Admin User creation be allowed?
                    serializer.validated_data["is_superuser"] = False    #Disallow creation of Superusers here
                    new_member = Member.objects.create_user(**serializer.validated_data)
                    print("Saved new Member:", new_member) #Debug
                    headers = self.get_success_headers(serializer.validated_data)    #Return HTTP Response Location Header if at least one member is created successfully
                    
                    print("Roles for Member:", roles_for_member) #Debug
                    try:    #In case of any exceptions while processing Roles, abort processing Roles for the current Member with an error
                        for role in roles_for_member:
                            print("Role:", role) #Debug
                            group, _ = Group.objects.get_or_create(name=role)  #TODO: Change to get after adding Role Master
                            FacilityMembership.objects.create(member=new_member, group=group, facility_id=facility_id)
                            if role=="Admin":
                                # Get or generate an Access Token for immediate login as Facility Admin
                                application = Application.objects.get(name="Password Grant")
                                expiry = datetime.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
                                access_token, _ = AccessToken.objects.get_or_create(application=application, scope="read write introspect", 
                                                                                    user=new_member, expires=expiry, token=generate_token())

                                # Include the access token in the response content for the current member if they have the Facility Admin Role
                                member_response["access_token"] = access_token.token
                        
                    # Handle potential exceptions during creation of Group, Membership or Access Token 
                    except Group.DoesNotExist:
                        role_error = {
                            "type": request.build_absolute_uri("/errors/bad-request-data"),
                            "title": "Member Role does not exist.",
                            "detail": f"The request contains a Member Role ('{role}') that is not recognized by the Access Management Service."
                        }
                    except Exception as e:
                        role_error = {
                            "type": request.build_absolute_uri("/errors/entity-creation-error"),
                            "title": "Failed to create a new Role, Membership or Access Token.",
                            "detail": repr(e) #Debug - Remove before release
                        }
                    
                    if role_error:    #If there was an error while creating Memberships for this Member, append username with error details to the Response Body
                        member_errors.update(role_error)
                        response_body.append(member_errors)
                    else:    #If Roles and Memberships were created successfully, add the new Member details to the Response
                        new_member_serializer = self.get_serializer(new_member)
                        member_response.update(new_member_serializer.data)    #Add Validated Data to the response content for the current member
                        response_body.append(member_response)
                    
                else:    #If validation fails for the current member being processed, append username with error details to the Response Body
                    member_errors.update(serializer.errors)
                    response_body.append(member_errors)
                
            # Handle potential exceptions during Member creation other than the specific 
            except Exception as e:
                member_errors.update({
                    "type": request.build_absolute_uri("/errors/entity-creation-error"),
                    "title": "Failed to create a new Member entity.",
                    "detail": f"{type(e).__name__}: {e}" #Debug - TODO: Remove before release
                })
                response_body.append(member_errors)
            
        # TODO: Enable Event publishing and processing.
        
        return Response(response_body, status=status.HTTP_201_CREATED, headers=headers)
    

    @action(detail=False, permission_classes=[TokenHasReadWriteScope])
    def list_members_of_facility(self, request, fid):
        """ Retrieve all existing Members of the specified Facility. Accessible only to Members of that Facility. """
        
        facility_membership = FacilityMembership.objects.filter(facility_id=fid).select_related("group").prefetch_related("member")
        distinct_members = {membership.member for membership in facility_membership}

        # Regroup the Queryset by Member and aggregate Group Names for each member into a list
        grouped_by_member = {}
        for membership in facility_membership:
            grouping_value = membership.member.pk
            if grouping_value not in grouped_by_member:
                grouped_by_member[grouping_value] = {'roles': []}
            grouped_by_member[grouping_value]['roles'].append(membership.group.name)
        
        # If the requesting User is a Superuser or a Member of the same Facility then proceed, else return 403 FORBIDDEN
        if request.user.is_superuser or any(mem.id == request.user.id for mem in distinct_members):
            members_serializer = self.get_serializer(distinct_members, many=True)
            
            response_body = { "members": members_serializer.data }
            for member in response_body["members"]:
                member |= grouped_by_member[member["id"]]
            
            return Response(response_body, status=status.HTTP_200_OK)
        else:
            error_body = {
                "type": request.build_absolute_uri("/errors/facility-level-access-only"),
                "title": "Access Denied.",
                "detail": "Only Superusers and Facility Members can access this data."
            }
            return Response(error_body, status=status.HTTP_403_FORBIDDEN)


    @action(detail=False, permission_classes=[TokenHasReadWriteScope])
    def get_membership_for_member(self, request, mid):
        """ 
        Retrieve all Facilities and respective Roles for the Member with the specified ID.
        Accessible only to Superusers and the Member in question.
        """

        membership_details = FacilityMembership.objects.filter(member__id=mid).prefetch_related("group")
        distinct_facility_ids = membership_details.values_list("facility_id", flat=True).distinct() #Dev Note: Returns QuerySet of UUIDs
        
        # If the requesting User is a Superuser or the Member in question then proceed, else return '403 FORBIDDEN'
        if request.user.is_superuser or mid == str(request.user.id):
            response_body = {}
            for fid_as_uuid in distinct_facility_ids:
                facility_id = fid_as_uuid.hex
                facility_membership = membership_details.filter(facility_id=facility_id)
                response_body["membership"] = { "facility_id": str(facility_id), "roles": facility_membership.values("group__name") }
            return Response(response_body, status=status.HTTP_200_OK)
        else:
            error_body = {
                "type": request.build_absolute_uri("/errors/superuser-and-self-access-only"),
                "title": "Access Denied.",
                "detail": "Only Superusers and the concerned Member can access this data."
            }
            return Response(error_body, status=status.HTTP_403_FORBIDDEN)


    @action(detail=False, permission_classes=[TokenHasReadWriteScope])
    def get_facility_roles_for_member(self, request, mid, fid):
        """ Retrieve all Roles for the Member with the specified ID at the specified Facility. Accessible only to Members of that Facility. """

        facility_membership = FacilityMembership.objects.filter(facility_id=fid).prefetch_related("group")
        distinct_member_ids = {membership.member_id for membership in facility_membership}
        print("Distinct Member IDs:", distinct_member_ids) #Debug

        # If the requesting User is a Superuser or a Member of the same Facility then proceed, else return 403 FORBIDDEN
        if request.user.is_superuser or request.user.id in distinct_member_ids:
            membership_of_interest = facility_membership.filter(member_id=mid)
            if membership_of_interest.exists():
                response_body = {"facility_id": fid, "member_id": mid, 
                                 "roles": list(membership_of_interest.values_list("group__name", flat=True))}
                return Response(response_body, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            error_body = {
                "type": request.build_absolute_uri("/errors/facility-level-access-only"),
                "title": "Access Denied.",
                "detail": "Only Superusers and Facility Members can access this data."
            }
            return Response(error_body, status=status.HTTP_403_FORBIDDEN)


    def retrieve_member_by_username(self, request, username):
        """ Get details for a specified Member of a Facility based on Username. """

        member = get_object_or_404(Member.objects.all(), username=username)    #Get Member by unique Username
        member_serializer = self.get_serializer(member)
        return Response(member_serializer.data, status=status.HTTP_200_OK)


    def update_member_by_username(self, request, username):
        """ Update properties of an existing Member based on their Username. """

        request_body = request.data
        member = get_object_or_404(Member.objects.all(), username=username)    #Get Member by unique Username
        # Note: The update_password method must be used to change the Password.
        # Note: Email ID update is disallowed since it is used as the unique UserName in some cases.
        member.name = request_body['name'].strip()
        member.mobile = request_body['mobile'].strip()
        member.save()

        # TODO: Enable Event publishing and processing.
        # # Publish Event indicating thar a member has been updated
        # member_serializer = self.get_serializer(member)
        # data_to_publish = { 'uniqueFacilityIdentificationNumber': request_body['facility_id'] }
        # data_to_publish.update(member_serializer.data)
        # publish(member.userRole.lower() + ' updated', data_to_publish)

        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=False, permission_classes=[TokenHasReadWriteScope])
    def update_password(self, request, username):
        """ Update the password for a registered Member. """

        # If the requesting User is a Superuser or the Member in question then proceed, else return 403 FORBIDDEN
        if not request.user.is_superuser and username != request.user.username:
            error_body = {
                "type": request.build_absolute_uri("/errors/superuser-and-self-access-only"),
                "title": "Access Denied.",
                "detail": "Only Superusers and the concerned Member can access this data."
            }
            return Response(error_body, status=status.HTTP_403_FORBIDDEN)
        
        # Decode the request body to access request parameters
        request_body = request.data
        password = request_body['password']
        confirm_password = request_body['confirm_password']
        # Validate password parameters
        if len(password) > 0:   #TODO: Enforce minimum password length?
            if password != confirm_password:
                error_body = {
                    "type": request.build_absolute_uri("/errors/password-confirmation-failure"),
                    "title": "Password confirmation failure.",
                    "detail": "Password and Password Confirmation must match."
                }
                return Response(error_body, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            error_body = {
                "type": request.build_absolute_uri("/errors/blank-password"),
                "title": "Password cannot be blank.",
                "detail": "A valid Password must be provided."
            }
            return Response(error_body, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                
        member = get_object_or_404(Member.objects.all(), username=username)    #Get Member by unique Username
        member.set_password(password)
        member.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)


    def deactivate_user_by_username(self, request, username):
        """
        Deactivate an existing, active User based on their Username.
        Only Superusers and the concerned Member are allowed to perform this operation.
        """
        
        member = get_object_or_404(Member.objects.all(), username=username)    #Get Member by unique Username
        
        # Check for various blocking conditions
        if not member.is_active:
            error_body = {
                "type": request.build_absolute_uri("/errors/cannot-deactivate-inactive-member"),
                "title": "Member is already Inactive.",
                "detail": "The specified username belongs to a member who is currently inactive.",
                "instance": request.build_absolute_uri(reverse("member_by_username", kwargs={'username':username}))
            }
            return Response(error_body, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # If the requesting User is not the Member in question, not a Superuser and not an Admin of that Facility, return 403 FORBIDDEN
        if username != request.user.username and not request.user.is_superuser:
            error_body = {
                "type": request.build_absolute_uri("/errors/superuser-and-self-access-only"),
                "title": "Access Denied.",
                "detail": "Only Superusers and the concerned Member can deactivate a Member."
            }
            return Response(error_body, status=status.HTTP_403_FORBIDDEN)
                
        member.is_active = False
        member.save()

        # TODO: Enable Event publishing and processing.
        # # Publish Event indicating thar a Member has been deactivated.
        # member_serializer = self.get_serializer(member)
        # data_to_publish = { 'uniqueFacilityIdentificationNumber': request_body['facility_id'] }
        # data_to_publish.update(member_serializer.data)
        # publish(member.userRole.lower() + ' deactivated', data_to_publish)

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    """ Defines CRUD operations on the Group entity managed only by the Superuser Role. """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [TokenHasReadWriteScope, IsTrustedClientPermission | IsSuperuserPermission]


class PermissionViewSet(viewsets.ModelViewSet):
    """ Defines CRUD operations on the Permission entity managed only by the Superuser Role. """

    queryset = Permission.objects.all()
    serializer_class = PermissionCodesSerializer
    permission_classes = [TokenHasReadWriteScope, IsTrustedClientPermission | IsSuperuserPermission]


class FacilityMembershipViewSet(viewsets.ModelViewSet):
    """ Defines CRUD operations on the FacilityMembership entity managed only by the Superuser or Facility Admin. """

    queryset = FacilityMembership.objects.all()
    serializer_class = FacilityMembershipSerializer
    permission_classes = [TokenHasReadWriteScope, IsTrustedClientPermission | IsSuperuserPermission]
