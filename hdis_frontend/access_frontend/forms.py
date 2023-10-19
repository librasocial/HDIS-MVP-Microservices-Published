from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


import re

def validate_mobile_number(value):
    if not re.match(r'^\d{10}$', value):
        raise ValidationError('Please enter a valid 10-digit mobile number')



class FacilityRegisterForm(forms.Form):
     facilityApplicantName=forms.CharField(label="Name",max_length=64)
     facilityApplicantEmail=forms.CharField(label="Email",validators=[validate_email],max_length=128)
     facilityApplicantMobile=forms.CharField(label="Mobile",validators=[validate_mobile_number])
     facilityApplicantCountry=forms.CharField(label="Country",max_length=64,initial="India")
     facilityApplicantCity=forms.CharField(label="City",max_length=64)
     facilityName=forms.CharField(label="Facility Name",max_length=128)
     facilityTypeCode=forms.ChoiceField(label="Facility Type", widget=forms.Select(attrs={'class': 'form-control'}))
     facilityInternalClass=forms.IntegerField(widget=forms.HiddenInput)
     facilityApplicantRemarks=forms.CharField(required=False,label="Remarks",max_length=128,widget=forms.Textarea(attrs={'rows': 5, 'cols': 30}))
   
     def clean_facilityTypeCode(self):
        value = self.cleaned_data['facilityTypeCode']
        return str(value)
     

class FacilityAddUserForm(forms.Form):
    userName=forms.CharField(label="Name",max_length=64)
    userEmail=forms.CharField(label="Email",validators=[validate_email],max_length=128)
    usertType=forms.ChoiceField(label="User Type", widget=forms.Select(attrs={'class': 'form-control'}))

    def clean_usertType(self):
        value = self.cleaned_data['user_type']
        return str(value)
    

class ServiceAddForm(forms.Form):
    #servicecategoryId= models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    serviceUnit = forms.CharField(max_length=50, label="Service Unit")
    serviceName = forms.CharField(max_length=50, label="Service Name")
    serviceShortName = forms.CharField(max_length=50, label="Service Short Name")
    usageType = forms.CharField(max_length=50, label="Usage Type") #oen time/time based etc
    serviceEffectiveDateFrom = forms.CharField(max_length=50, label="Effective From")
    serviceEffectiveDateTo = forms.CharField(max_length=50, label="Effective Till")
    serviceCost = forms.CharField(label="Service Cost")
    serviceMaximumRate = forms.CharField(label="Service Maximum Rate")
    serviceMinimumRate = forms.CharField(label="Service Minimum Rate")
    isInventory=forms.BooleanField()
    isActive = forms.BooleanField()
    isTaxable = forms.BooleanField() #if taxable then tax code to be adeed
    discountAllowed = forms.BooleanField()

class ServiceEditForm(forms.Form):
    primaryKey=forms.CharField(widget=forms.HiddenInput)
    serviceUnit = forms.CharField(max_length=50, label="Service Unit")
    serviceName = forms.CharField(max_length=50, label="Service Name")
    serviceShortName = forms.CharField(max_length=50, label="Service Short Name")
    usageType = forms.CharField(max_length=50, label="Usage Type") #oen time/time based etc
    serviceEffectiveDateFrom = forms.CharField(max_length=50, label="Effective From")
    serviceEffectiveDateTo = forms.CharField(max_length=50, label="Effective Till")
    serviceCost = forms.CharField(label="Service Cost")
    serviceMaximumRate = forms.CharField(label="Service Maximum Rate")
    serviceMinimumRate = forms.CharField(label="Service Minimum Rate")
    isInventory=forms.BooleanField()
    isActive = forms.BooleanField()
    isTaxable = forms.BooleanField() #if taxable then tax code to be adeed
    discountAllowed = forms.BooleanField()

    
class FacilityEditUserForm(forms.Form):
    memberName=forms.CharField(label="Name",max_length=64)
    memberEmail=forms.CharField(label="Email",validators=[validate_email],max_length=128)
    memberMobile=forms.CharField(label="Mobile",validators=[validate_mobile_number])
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
    
class FacilityEditDoctorForm(forms.Form):
    memberName=forms.CharField(label="Name",max_length=64)
    memberEmail=forms.CharField(label="Email",validators=[validate_email],max_length=128)
    memberMobile=forms.CharField(label="Mobile",validators=[validate_mobile_number])
    password = forms.CharField(widget=forms.PasswordInput(),required=False)
    confirm_password=forms.CharField(widget=forms.PasswordInput(),required=False)
    doctorRegistrationNumber=forms.CharField(label="Registration Number",required=False)
    doctorRegistrationCertificate=forms.FileField(label="Registration Certificate",required=False)
    languagesKnown=forms.CharField(label="Languages Known",required=False)
    currentCity=forms.CharField(label="Current city",required=False)
    doctorSpeciality=forms.ChoiceField(label="Speciality", widget=forms.Select(attrs={'class': 'form-control'}),required=False)
    doctorImage=forms.FileField(label="Doctor Image",required=False)
    doctorBankDetails=forms.CharField(label="Bank Account Details",required=False)
    doctorSignatures=forms.FileField(label="Doctor Signature",required=False)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        doctorSpeciality=cleaned_data.get('doctorSpeciality')
        choices = self.fields['doctorSpeciality'].choices
        print(doctorSpeciality)

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
            #raise ValidationError("Passwords do not match.")

        return cleaned_data
    def clean_file(self):
        doctorRegistrationCertificate = self.cleaned_data.get('doctorRegistrationCertificate')
        if doctorRegistrationCertificate:
            # Perform custom file validation here
            if doctorRegistrationCertificate.size > 1024 * 1024:  # Example: Limit file size to 1MB
                raise forms.ValidationError("File size exceeds the limit.")

        return doctorRegistrationCertificate
    
    def clean_doctorSpeciality(self):
        print('in cleaning data')
        data=self.cleaned_data['doctorSpeciality']
        return data





