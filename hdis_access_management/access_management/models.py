from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group

class MemberManager(BaseUserManager):
    """Custom Manager class for the Member class that extends User."""

    def create_user(self, username, name, password=None, **extra_fields):
        """ This Manager method should be invoked to create new Member instances instead of directly calling  
            "save()" on a Member instance to ensure that the password is properly stored in hashed form.
        """
        
        if not username:
            raise ValueError("The 'username' field must be set")
        member = self.model(username=username, name=name, **extra_fields)
        member.clean()    #Normalizes username
        member.email = self.normalize_email(member.email)    #Ensures Domain part is all-lowercase
        member.set_password(password)    #Converts the password into a hash for storage
        member.save(using=self._db)
        return member

    def create_superuser(self, username, name, password=None, **extra_fields):
        """ This Manager method should be invoked to create a new Superuser Member instance. 
            It is automatically invoked when creating a superuser through the command-line through manage.py.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, name, password, **extra_fields)


class Member(AbstractUser):
    """Customized substitute for the standard User class."""
    
    # Remove unwanted fields inherited from AbstractUser
    first_name = None
    last_name = None
    # Add new properties
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10, blank=True, default='')
    
    objects = MemberManager()
    REQUIRED_FIELDS = ['name']
    # Note: Email and Mobile are optional.

    def __str__(self):
        return self.username


class FacilityMembership(models.Model):
    """Maps Users to the Roles they are allocated to at specific Facilities."""

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="memberships")
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    facility_id = models.UUIDField()
    
    class Meta:
        verbose_name = 'Facility Membership'
        verbose_name_plural = 'Facility Memberships'
        db_table = 'facility_membership'
    def __str__(self):
        return f"{self.member}|{self.group}|{self.facility_id}"


class RolePermissions(models.Model):
    """For each Role, defines the  Permissions applicable at a Facility."""

    role_code = models.CharField(max_length=64)
    facility_permission = models.CharField(max_length=64)

    class Meta:
        managed = False
        unique_together = ("role_code", "facility_permission")
        db_table = 'role_permissions'
    def __str__(self):
        return str(self.role_code + "/" + self.facility_permission)
