from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import string
import secrets
import base64
import uuid

# Create your models here.

class Facility(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True,default=uuid.uuid4)
    uniqueFacilityIdentificationNumber = models.UUIDField(default=uuid.uuid4)
    facilityTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    facilityServiceCode = models.CharField(max_length=18, blank=True, null=True)
    departmentName = models.CharField(max_length=99, blank=True, null=True)
    referralFacilityIdentificationNumber = models.CharField(max_length=10, blank=True, null=True)
    referralFacilityTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    referralFromFacilityIdentificationNumber = models.CharField(max_length=10, blank=True, null=True)
    referralFromFacilityTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    facilityGlobalUniqueIdentifier = models.BinaryField(blank=True, null=True)
    facilitySpecialtyCode = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    class Meta:
        verbose_name_plural = 'Facility'
        db_table = 'Facility'
    def __str__(self):
        return str(self.PrimaryKey)
    
class Extra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    facilityId=models.ManyToManyField(Facility)
    userMobile=models.CharField(max_length=64,blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Extra.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.extra.save()

    
"""
class User(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId=models.ManyToManyField(Facility)
    userRole=models.CharField(max_length=64)
    userName=models.CharField(max_length=64)
    userEmail=models.CharField(max_length=128,blank=True)
    userMobile=models.CharField(max_length=64,blank=True)
    userPassword=models.CharField(max_length=128,blank=True)
    userPasswordToken=models.CharField(max_length=128,blank=True)
    userResetToken=models.CharField(max_length=128,blank=True)
    is_anonymous=models.BooleanField(default=False)
    is_authenticated=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)

    USERNAME_FIELD = 'userEmail'
    REQUIRED_FIELDS = ['userRole','userName']
    class Meta:
        verbose_name_plural = 'User'
        db_table = 'User'
    def __str__(self):
        return self.userName

    def set_password(self, password):
        print("saving password")
        self.userPassword = make_password(password)

    def check_password(self, password):
        print("checking password")
        return check_password(password, self.userPassword)
    
    def set_default_password(self,length=12):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        self.userPassword = ''.join(secrets.choice(alphabet) for i in range(length))

    def set_reset_token(self):
    
        # Generate random bytes
        random_bytes = secrets.token_bytes(16)
        # Convert bytes to base64-encoded string
        base64_bytes = base64.b64encode(random_bytes).decode('utf-8')
        # Remove padding characters
        base64_string = base64_bytes.replace('=', '')
        # Check if the string contains only alphanumeric characters
        self.userResetToken= base64_string

"""    
        

    

