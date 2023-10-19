from django.shortcuts import render,redirect
import requests
import json
import random
from django.conf import settings
from access_frontend.views import login
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime,timedelta
from hdis_frontend.decorators import jwt_token_required
# Create your views here.
@jwt_token_required
def search_patient(request,data,status):
    if status!=200:
        return redirect(login) 
    else: 
        if request.method == 'GET':
            context={"user":data}
            return render(request, 'visit_management/search_patient.html', context)
        else:
            access_token = request.session.get('access_token')
            print(request.POST)
            if 'search_patient' in request.POST:
                lfpId = request.POST.get("patient_id")
                url = settings.HDIS_PATIENT_REGISTRATION + "/api/patients/facilitySearch/" + lfpId
                values={}
                values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
                values['userId']=request.session['userId']
                values['userGroup']=request.session['userGroup']
                values['facilityTypeCode']=request.session['facilityTypeCode']
                payload = json.dumps(values)
                print(url)
                r = requests.get(url,data=payload,
                                 headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                          'Authorization': f'Bearer {access_token}'})
                print (r.status_code)
                if r.status_code == 200:
                    # print('user is authenticated')
                    patient_list = json.loads(r.content.decode('utf-8'))
                    print(patient_list)
                    uhid = patient_list.personId.uniqueHealthIdentificationId
                    print(uhid)
                    # search for appointment
                    url = settings.HDIS_APPOINTMENT_MANAGEMENT + "/api/get_patient_appointment/"
                    content = {"uniqueHealthIdentificationId": uhid}
                    values = dict(content)
                    values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
                    values['userId']=request.session['userId']
                    values['userGroup']=request.session['userGroup']
                    values['facilityTypeCode']=request.session['facilityTypeCode']
                    payload = json.dumps(values)
                    access_token = request.session.get('access_token')
                    r = requests.post(url, data=payload,
                                      headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                               'Authorization': f'Bearer {access_token}'})
                    a = r.content.decode('utf-8')
                    appointment_list = json.loads(a)
                    print(appointment_list)
                    print(patient_list)
                    context = {'user': data, 'patients': patient_list[0], 'appointments': appointment_list}
                    return render(request, 'visit_management/select_patient.html', context)
                else:
                    print(1)

            elif 'speciality_selected' in request.POST:
                uhid=request.POST.get("uhid")
                url = settings.HDIS_PATIENT_REGISTRATION+"/api/patients/uhid/" + str(uhid)
                print(url)
                values={}
                values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
                values['userId']=request.session['userId']
                values['userGroup']=request.session['userGroup']
                values['facilityTypeCode']=request.session['facilityTypeCode']
                payload = json.dumps(values)
                r = requests.get(url,data=payload,
                                 headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                          'Authorization': f'Bearer {access_token}'})
                if r.status_code==200:
                    #print('user is authenticated')
                    patient_list = json.loads(r.content.decode('utf-8'))
                    #search for appointment
                    url = settings.HDIS_APPOINTMENT_MANAGEMENT+"/api/get_patient_appointment/"
                    content = {"uniqueHealthIdentificationId":uhid}
                    values = dict(content)
                    values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
                    values['userId']=request.session['userId']
                    values['userGroup']=request.session['userGroup']
                    values['facilityTypeCode']=request.session['facilityTypeCode']
                    payload = json.dumps(values)
                    access_token = request.session.get('access_token')
                    r = requests.post(url,data=payload,
                            headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
                    a = r.content.decode('utf-8')
                    appointment_list=json.loads(a)
                    print(appointment_list)
                    pat=json.loads(patient_list) # need to check wht this is done
                    context = {'user': data, 'patients': pat[0],'appointments':appointment_list}
                    return render(request, 'visit_management/select_patient.html', context)
                else:
                    print(1)

@jwt_token_required
def checkin(request,data,status):
    if status!=200:
        return redirect(login) 
    else:
        #call visit management
        details=request.POST.items()
        url = settings.HDIS_VISIT_MANAGEMENT+"/api/visit_check_in/"
        values = dict(details)
        values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
        values['userId']=request.session['userId']
        values['userGroup']=request.session['userGroup']
        values['facilityTypeCode']=request.session['facilityTypeCode']
        payload = json.dumps(values)
        print(payload)
        access_token = request.session.get('access_token')
        r = requests.post(url,data=payload,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
        
        if r.status_code==200:
        
                access_token = request.session.get('access_token')
                url = settings.HDIS_QUEUE_MANAGEMENT+"/api/getToken/"

                r = requests.post(url,data=payload,
                            headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
                a = r.content.decode('utf-8')
                visit_data=json.loads(a)


                url = settings.HDIS_PATIENT_REGISTRATION+"/api/patients/"+str(values['PatientId'])
                print(url)
                values={}
                values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
                values['userId']=request.session['userId']
                values['userGroup']=request.session['userGroup']
                values['facilityTypeCode']=request.session['facilityTypeCode']
                values['token_number'] = random.randrange(1, 50, 3)
                payload = json.dumps(values)
                r=requests.get(url,data=payload,
                            headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
            
                patient_details = json.loads(r.content.decode('utf-8'))
                print(patient_details)
                context={"user":data,'token_details':values,"visit":json.loads(visit_data),'patient':json.loads(patient_details)}
                #print(context)
                return render(request, 'visit_management/token_generated.html', context)
        else:
            pass




