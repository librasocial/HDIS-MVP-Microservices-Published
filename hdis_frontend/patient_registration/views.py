import json
import requests
import base64
from django.contrib import messages
from django.shortcuts import render, redirect
from appointment_booking.views import book_appointment
from django.http import HttpResponseRedirect
from access_frontend.views import login
from django.conf import settings
from hdis_frontend.decorators import jwt_token_required

# Create your views here.
from datetime import datetime, timezone, date, timedelta

#@jwt_token_required
def register(request):
    if request.session.get('access_token'):
        if request.method == 'POST':

            if 'patient_registration' in request.POST:
                return render(request, 'patient_registration/registration_options.html')
            elif 'register_with' in request.POST:
                context = {}
                content = list(request.POST.items())
                values = dict(content)
                context['register_with'] = values['registration_options']
                return render(request, 'patient_registration/register.html', context)
        else:
            return render(request, 'patient_registration/registration_options.html')
    else:
        return redirect(login)
#@jwt_token_required
def get_or_create_patient(request):
    if request.session.get('access_token'):
        content = list(request.POST.items())
        values = dict(content)
        #Add Abha ID
        print("here now")
        print(values)
        access_token = request.session.get('access_token')
        url = settings.HDIS_PATIENT_REGISTRATION+"/patients/"
        values['facility_id']=request.session['uniqueFacilityIdentificationNumber']
        payload = json.dumps(values)
        r = requests.post(url, data=payload,
                            headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                     'Authorization': f'Bearer {access_token}'})
        a = json.loads(r.content.decode('utf-8'))
        print("am i here")
        print(a)
        print (r.status_code)
        if r.status_code == 300:
            print("lost in space")
            patient_list = json.loads(a)
            messages.add_message(request, messages.SUCCESS,
                                    'Patient already registered, please select the user from the list below')
        else:
            patient_list = [a]
            messages.add_message(request, messages.SUCCESS,
                                 'Patient successfully registered')
        context = {"patient_list": patient_list}
        return render(request, 'appointment_booking/select_patient.html', context)
    else:
        return redirect(login)