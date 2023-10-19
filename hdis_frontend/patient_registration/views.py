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

@jwt_token_required
def register(request,data,status):
    if request.method == 'POST':

        if 'patient_registration' in request.POST:
            
                if status==200:
                    print('user is authenticated')
                    user={}
                    user["is_authenticated"]=True
                    print(data['groups'][0]['name'])
                    user["role"]=data['groups'][0]['name']
                    authenticated=True
                    context={'user':user}
                    return registernow(request)

                else:
                    
                    return redirect(login)
        elif 'register_with' in request.POST:
            if status == 200:
                user = {}
                user["is_authenticated"] = True
                context = {'user': user}
                content = list(request.POST.items())
                values = dict(content)
                context['register_with'] = values['registration_options']
                return render(request, 'patient_registration/register.html', context)
            else:
                return redirect(login)
    else:
        if status==200:
            user={}
            user["is_authenticated"]=True
            context={'user':user}
            return render(request, 'patient_registration/registration_options.html',context)
        else:
            return redirect(login)
@jwt_token_required
def registernow(request,data,status):
    facilityId=data['extra']['facilityId'][0]['uniqueFacilityIdentificationNumber']
    content = list(request.POST.items())
    values = dict(content)
    #Add Abha ID
    print("here now")

    access_token = request.session.get('access_token')
    url = settings.HDIS_PATIENT_REGISTRATION+"/api/patients"
    #values['facilityID'] = facilityId
    values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
    values['userId']=request.session['userId']
    values['userGroup']=request.session['userGroup']
    values['facilityTypeCode']=request.session['facilityTypeCode']

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
        patient_list = [json.loads(a)]
        messages.add_message(request, messages.SUCCESS,
                             'Patient successfully registered')
    context = {"patient_list": patient_list, "user": data}
    return render(request, 'appointment_booking/select_patient.html', context)