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
import pytz


# Create your views here.
@jwt_token_required
def book_appointment_confirm(request,data,status):
    if status!=200:
        return redirect(login) 
    else:
        content = list(request.POST.items())
        values_post = dict(content)
        print(values_post)
        url = settings.HDIS_APPOINTMENT_MANAGEMENT+"/api/create_appointment/"
        content = {"uniqueIndividualHealthCareProviderNumber":values_post['lhpn'],"uniqueHealthIdentificationId":values_post['patientid'],"date":values_post['date'],"time":values_post['time']}
        values = dict(content)
        values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
        values['userId']=request.session['userId']
        values['userGroup']=request.session['userGroup']
        values['facilityTypeCode']=request.session['facilityTypeCode']   
        payload = json.dumps(values)

        access_token = request.session.get('access_token')
        r = requests.get(url,data=payload,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
        a = r.content.decode('utf-8')
        appointment_details=json.loads(a)

        context={"user":data, 'appointment_details':json.loads(appointment_details)}
        print(context)

        return render(request, 'appointment_booking/appointment_confirm.html', context)
    

def get_closest_15_minute_interval():
    # Get the current time in UTC
    current_time = datetime.now(pytz.utc)

    # Convert the current time to the India timezone
    india_tz = pytz.timezone('Asia/Kolkata')
    current_time = current_time.astimezone(india_tz)

    # Get the current minute in the India timezone
    current_minute = current_time.minute

    # Calculate the number of minutes past the nearest 15-minute interval
    remainder = current_minute % 15

    # Determine whether to round up or down based on the remainder
    if remainder < 8:
        rounded_minute = current_minute - remainder
    else:
        rounded_minute = current_minute + (15 - remainder)

    if rounded_minute==60:
        rounded_minute=45


    # Create a new time object with the rounded minute value
    rounded_time = current_time.replace(minute=rounded_minute, second=0, microsecond=0)

    # Format the time as HH:MM string
    formatted_time = rounded_time.strftime('%H:%M')

    return formatted_time


@jwt_token_required
def book_appointment_next_confirm(request,data,status):
    if status!=200:
        return redirect(login) 
    else:
        content = list(request.POST.items())
        values_post = dict(content)
        print(values_post)
        url = settings.HDIS_APPOINTMENT_MANAGEMENT+"/api/create_appointment/"
        providerLHID=values_post['lhpn']
        PatientId=values_post['patientid']
        appt_date=datetime.today().strftime('%m/%d/%Y')
        appt_time=get_closest_15_minute_interval()
        appt_date_time=datetime.today().strftime('%Y-%m-%d')+" "+appt_time
        content = {"uniqueIndividualHealthCareProviderNumber":providerLHID,"uniqueHealthIdentificationId":PatientId,"date":appt_date,"time":appt_time}
        values = dict(content)
        values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
        values['userId']=request.session['userId']
        values['userGroup']=request.session['userGroup']
        values['facilityTypeCode']=request.session['facilityTypeCode']   
        payload = json.dumps(values)

        access_token = request.session.get('access_token')
        r = requests.get(url,data=payload,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
        a = r.content.decode('utf-8')

        if r.status_code==201:
            #checkin
            url = settings.HDIS_VISIT_MANAGEMENT+"/api/visit_check_in/"
            values = {}
            values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
            values['userId']=request.session['userId']
            values['userGroup']=request.session['userGroup']
            values['facilityTypeCode']=request.session['facilityTypeCode']
            values['providerLHID']=providerLHID
            values['PatientId']=PatientId
            values['appointmentdatetime']=appt_date_time
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


                url = settings.HDIS_PATIENT_REGISTRATION+"/api/patients/"+str(PatientId)
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

        else:
            appointment_details=json.loads(a)

            context={"user":data, 'appointment_details':json.loads(appointment_details)}
            print(context)
            return render(request, 'appointment_booking/appointment_confirm.html', context)


@jwt_token_required
def book_appointment(request,data,status):
    
    if status!=200:
        return redirect(login) 
    else:
        content = list(request.POST.items())
        
        values = dict(content)
        values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
        values['userId']=request.session['userId']
        values['userGroup']=request.session['userGroup']
        values['facilityTypeCode']=request.session['facilityTypeCode']
        payload = json.dumps(values)
        url = settings.HDIS_DOCTOR_ADMINISTRATION+"/api/doctors/"
        access_token = request.session.get('access_token')
        r = requests.get(url, data=payload,headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                       'Authorization': f'Bearer {access_token}'})
        a = r.content.decode('utf-8')
        print(r.status_code)
        b=json.loads(a)
        print(b)



      

        pId=request.POST.get("PatientId")
        print('pid is '+pId)

        url = settings.HDIS_PATIENT_REGISTRATION+"/api/patients/"+str(pId)
        print(url)
        values={}
        values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
        values['userId']=request.session['userId']
        values['userGroup']=request.session['userGroup']
        values['facilityTypeCode']=request.session['facilityTypeCode']
        payload = json.dumps(values)
        r=requests.get(url,data=payload,
                       headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
       
        patient_details = json.loads(r.content.decode('utf-8'))
        print(patient_details)
       # patient_details['UHID']=request.POST.get("PatientUHId")
        print('now now')
        print(patient_details)

        context={"user":data,'patient_details':json.loads(patient_details),'doctors':b}
        print(context)

        return render(request, 'appointment_booking/book_appointment.html', context)


def getProviderFreeSlots(request):
    lhpn=request.GET['lhpn']
    #Get any appointments for this doctor
    url = settings.HDIS_APPOINTMENT_MANAGEMENT+"/api/get_provider_appointment/"
    content = {"uniqueIndividualHealthCareProviderNumber":lhpn,"requestdate":request.GET['day']}
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
    ret=json.loads(a)
    print(ret)
    busy_slots=[]
    if r.status_code==200:
        for busy in ret:
            datetime_obj = datetime.strptime(busy['AppointmentSessionStartTime'],'%Y-%m-%d %H:%M')

            # Extract time in H:M format
            time_str = datetime_obj.strftime('%H:%M')
            busy_slots.append(time_str)

    print('busy slots')
    print(busy_slots)    


    thisdate=datetime.strptime(request.GET['day'], '%m/%d/%Y')
    print(thisdate)
    days_of_week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    
    
    day_of_week = thisdate.weekday()

    print(day_of_week)

    day=days_of_week[day_of_week]
    url = settings.HDIS_SLOT_MASTER+"/api/doctors/"+lhpn+"/"+day
    r = requests.get(url,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
    a = r.content.decode('utf-8')
    print(r.status_code)
    print('slot master')
    c=json.loads(a)
    daily_slot_list=c["daily_slot_list"]
    print(daily_slot_list[0])
    slot_list=daily_slot_list[0]
    print(slot_list)
    startTime=slot_list['dayOfTheWeekSlotStartTime']
    endTime=slot_list['dayOfTheWeekSlotEndTime']
    duration=slot_list['dayOfTheWeekSlotDuration']
    print(startTime)
    print(endTime)
    print(duration)

    clock_time = startTime
    time1_obj = datetime.strptime(clock_time, '%H:%M')
    time2_obj = datetime.strptime(endTime, '%H:%M')
    time2_obj=time2_obj-timedelta(minutes=int(duration)+1)
    slots=[] 
    
    if clock_time not in busy_slots:
        slot_free_var={"state":"free","time":clock_time}
        slots.append(slot_free_var)
    else:
        slot_busy_var={"state":"busy","time":clock_time}
        slots.append(slot_busy_var)

    
    while time2_obj>time1_obj:
        hours, minutes = clock_time.split(':')
        hours = int(hours)
        minutes = int(minutes)

        minutes_to_add = int(duration)
        total_minutes = hours * 60 + minutes + minutes_to_add
        total_hours = total_minutes // 60
        remaining_minutes = total_minutes % 60

        new_clock_time = f"{total_hours:02}:{remaining_minutes:02}"
        print(new_clock_time)
       


        if new_clock_time not in busy_slots:
            slot_free_var={"state":"free","time":new_clock_time}
            slots.append(slot_free_var)
        else:
            slot_busy_var={"state":"busy","time":new_clock_time}
            slots.append(slot_busy_var)

        
            
        time1_obj = datetime.strptime(new_clock_time, '%H:%M')
        clock_time=new_clock_time

    print(slots)




    





    return JsonResponse(slots, safe=False)

def token_generated(request,data,status):
    if status!=200:
        return redirect(login) 
    else: 

        content = list(request.POST.items())
        values = dict(content)
        values['token_number'] = random.randrange(1, 50, 3)
        context={"user":data,'token_details':values}
        return render(request, 'appointment_booking/token_generated.html', context)

@jwt_token_required
def search_patient(request,data,status):
   
    if status!=200:
        return redirect(login) 
    else: 
        if request.method == 'GET':
            context={"user":data}
            return render(request, 'appointment_booking/search_patient.html', context)
        else:
            uhid=request.POST.get("uhid")
            url = settings.HDIS_PATIENT_REGISTRATION+"/api/patients/uhid/" + str(uhid)
            print(url)

            r = requests.get(url)
            
            
            #print('user is authenticated')
            patient_list = json.loads(r.content.decode('utf-8'))
            print("here in")
            print(patient_list)
            context = {'user': data, 'patient_list': patient_list}
            return render(request, 'appointment_booking/select_patient.html', context)

@jwt_token_required
def select_patient(request,data,status):

    #get speciality and doctors for facility

    
    
    if status!=200:
        return redirect(login) 
    else: 

        content = list(request.POST.items())
        context={"user":data}
        return render(request, 'appointment_booking/select_patient.html', context)





    


