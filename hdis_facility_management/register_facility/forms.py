from django import forms
from .models import *

class facilityRegistrationForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
       
    fields = "__all__"
    facility_types = [('', 'Select Facility Type')]
    for type in facilityType.objects.all():
        type_tuple = (type.facilityTypeDescription, type.facilityTypeDescription)
        facility_types.append(type_tuple)
    type_final = tuple(facility_types)

    widgets = {
        'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name', 'style': "margin:0px 20px 10px 0px"}),
        'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'style': "margin:0px 20px 10px 0px"}),
        'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'style': "margin:0px 20px 10px 0px"}),
        'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'style': "margin:0px 20px 10px 0px"}),
        'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country', 'style': "margin:0px 20px 10px 0px"}),
        'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City', 'style': "margin:0px 20px 10px 0px"}),
        'organisation_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organisation Name', 'style': "margin:0px 20px 10px 0px"}),
        'facility_type': forms.Select(choices=type_final, attrs={'class': 'form-control', 'placeholder': 'Facility Type', 'style': "margin:0px 20px 10px 0px"}),
        'remarks': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'style': 'margin:0px 20px 10px 0px'}),
    }


    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        for field in self.fields:
            self.fields[str(field)].label = ''
            if field == 'remarks':
                pass
            else:
                self.fields[str(field)].required = True
