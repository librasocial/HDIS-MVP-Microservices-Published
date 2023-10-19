import json
import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from appointment_booking.views import book_appointment
from django.http import HttpResponseRedirect
from django.contrib import messages
from access_frontend.views import login
def doctor_list(request):

    value = request.COOKIES.get('x-access-token')
    if value is None:
        return redirect(login)

    else:
        print(value)
   

        #return render(request, 'doctor_administration/register.html',context)

    url = settings.HDIS_DOCTOR_ADMINISTRATION+"/api/doctors/"
    r = requests.get(url,headers={'Content-type': 'application/json', 'Accept': 'application/json','x-access-token':value})
    a = r.content.decode('utf-8')
    print(r.status_code)
    if r.status_code==200:

        user={"is_authenticated":True}
        authenticated=True
        context={'user':user,'doctor_list': json.loads(a)}
        print(a)
        return render(request, 'doctor_administration/doctors_pending_activation.html', context)

    else:
        user={"is_authenticated":False}
        authenticated=False
        context={'user':user}
        return redirect(login)
        
   




   

def doctor_details(request, dId):

    value = request.COOKIES.get('x-access-token')
    if value is None:
        return redirect(login)

    else:
        print(value)

    url = settings.HDIS_DOCTOR_ADMINISTRATION+"/api/doctors_detail/" + dId
    r = requests.get(url,headers={'Content-type': 'application/json', 'Accept': 'application/json','x-access-token':value})
    a = r.content.decode('utf-8')

    print(dId)

    url = settings.HDIS_SLOT_MASTER+"/api/doctors/" + dId
    k = requests.get(url,headers={'Content-type': 'application/json', 'Accept': 'application/json','x-access-token':value})
    b = k.content.decode('utf-8')
    return render(request, 'doctor_administration/doctor_onboarding.html', {'doctor_details': json.loads(a), 'doctor_slots':json.loads(b)})

def doctor_details_update(request, dId):
    messages.add_message(request, messages.SUCCESS,
                         'Doctor onboarded successfully')
    return redirect(doctor_list)
def facility_field_check(request, fId):
    url = settings.HDIS_DOCTOR_ADMINISTRATION+"/api/doctor_field_check/" + fId
    k = requests.get(url)
    b = k.content.decode('utf-8')
    return render(request, 'doctor_administration/doctor_fields_needed.html',
                  {'doctor_fields': json.loads(b)})

def facility_field_check_update(request, fId):
    if request.method == 'POST':
        content = list(request.POST.items())
        values = dict(content)
        doctor_fields = {}
        try:
            doctor_fields['language'] = True
        except KeyError:
            doctor_fields['language'] = False
        try:
            doctor_fields['city'] = True
        except KeyError:
            doctor_fields['city'] = False
        try:
            doctor_fields['speciality'] = True
        except KeyError:
            doctor_fields['speciality'] = False
        try:
            doctor_fields['qualification'] = True
        except KeyError:
            doctor_fields['qualification'] = False
        try:
            doctor_fields['description'] = True
        except KeyError:
            doctor_fields['description'] = False
        try:
            doctor_fields['image'] = True
        except KeyError:
            doctor_fields['image'] = False
        try:
            doctor_fields['sign'] = True
        except KeyError:
            doctor_fields['sign'] = False
        try:
            doctor_fields['schedule'] = True
        except KeyError:
            doctor_fields['schedule'] = False
        try:
            doctor_fields['bankDetails'] = True
        except KeyError:
            doctor_fields['bankDetails'] = False
        try:
            doctor_fields['leaves'] = True
        except KeyError:
            doctor_fields['leaves'] = False
        url = settings.HDIS_DOCTOR_ADMINISTRATION+"/api/doctor_field_check/" + fId
        r = requests.put(url, data = json.dumps(doctor_fields),headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        messages.add_message(request, messages.SUCCESS,
                             'Field requirement successfully updated')
        return redirect(doctor_list)
    else:
        messages.add_message(request, messages.SUCCESS,
                             'Bad request method')
        return redirect(doctor_list)

