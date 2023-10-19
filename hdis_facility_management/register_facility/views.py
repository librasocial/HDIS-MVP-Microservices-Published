from django.shortcuts import render
from .forms import *
# Create your views here.
def hospitals_clinics(request):
    return render(request, 'register_facility/select_services.html')

def diagnostic_labs(request):
    return render(request, 'register_facility/select_services.html')

def pharmacies(request):
    return render(request, 'register_facility/select_services.html')

def register_facility(request):
    if request.method == 'POST':
        form = facilityRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'register_facility/select_microservices.html', {'facilityType': form.cleaned_data['facility_type']})
    else:
        form = facilityRegistrationForm()
        return render(request, 'register_facility/register_facility.html', {'form': form})

def select_microservices(request):
    return render(request, 'register_facility/select_microservices.html')
