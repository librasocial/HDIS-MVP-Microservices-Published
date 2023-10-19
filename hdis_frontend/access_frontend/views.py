import json
import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from datetime import datetime
from access_frontend.forms import FacilityRegisterForm,FacilityAddUserForm,FacilityEditUserForm,FacilityEditDoctorForm
from django.core.serializers import serialize
from hdis_frontend.decorators import jwt_token_required
from .models import SpecialityType
from django.utils.datastructures import MultiValueDictKeyError
import time

############### To Do ##########################
# Add additional fields in doctor profile
#After adding new user , if he is doctor go to edit profile







# Create your views here.

def login(request):
    from patient_registration.views import register

    if request.method=='POST' :


        url = settings.HDIS_AUTH_SERVER+"/access/token/"
        print(url)
        content = list(request.POST.items())
        values = dict(content)
        payload = json.dumps(values)
        print(payload)
        r = requests.post(url, data=payload,
                            headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        a = r.content.decode('utf-8')
        data=json.loads(a)
        user={}

        print(r.status_code)
        print(data)
        if r.status_code==200:

            print(data)
            # save tokens,userid and uniquefacility number in session
            request.session['access_token'] = data['access']
            request.session['refresh_token'] = data['refresh']
            request.session['userId']=data['user']['username']
            request.session['uniqueFacilityIdentificationNumber']=data['user']['extra']['facilityId'][0]['uniqueFacilityIdentificationNumber']
            request.session['userGroup']=data['user']['groups'][0]['name']
            request.session['facilityTypeCode']=data['user']['extra']['facilityId'][0]['facilityTypeCode']
            user=data['user']
            authenticated=True
            context={'user':data}

        else:
            authenticated=False
            messages=[]
            messages.append('Error :Please check email/password')
            context={'user':user,'messages':messages}
            redirect(login)

        if authenticated==True :
            
            if any(d['name'] == 'Super' for d in data['user']['groups']):
                return redirect(superadmin)
            elif any(d['name'] == 'Front Desk' for d in data['user']['groups']):
                return redirect(front_desk_home)
            elif any(d['name'] == 'Nurse' for d in data['user']['groups']):
                response = redirect(nurse_profile)
            elif any(d['name'] == 'Doctor' for d in data['user']['groups']):
                #fetch providerID and save in cookie
                #request.session['userid']=user['userid']
                #request.session['tenantID']=user['tenantID']


                response = redirect(doctor_profile)
            else: 
                #response=redirect(register)
                print('redirecting to dashboard')
                response= redirect(dashboard)


        else:
            response=  render(request,'access_frontend/login.html',context)

            
        return response

    else:

      
        
        return render(request,'access_frontend/login.html')


@jwt_token_required                
def doctor_profile(request,data,status):
    if status!=200:
        return redirect(login)

    else:

        #request.session['tenantID'] - will give facility id
        #get facility details
        facilityId=data['extra']['facilityId'][0]['uniqueFacilityIdentificationNumber']
        facility_details = 0
        #get doctor user details (how do we get dId)

        content={}
        values = dict(content)
        values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
        values['userId']=request.session['userId']
        values['userGroup']=request.session['userGroup']
        values['facilityTypeCode']=request.session['facilityTypeCode']
        payload = json.dumps(values)



        context = {}
        dId = data['username']
        url = settings.HDIS_DOCTOR_ADMINISTRATION + "/api/doctor_provider_details/" + dId

        access_token = request.session.get('access_token')
        r = requests.get(url,data=payload,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})

        a = r.content.decode('utf-8')
        doctor_details = json.loads(a)
        print(doctor_details)
        #get visit details for the facility+doctor+date (give option to select date and update the list of visits
        date = datetime.now().strftime("%Y-%m-%d")
        url_consult = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective/" + doctor_details['facilityId']['uniqueFacilityIdentificationNumber'] + "/" + doctor_details['uniqueIndividualHealthCareProviderNumber'] + "/" + date
        print(url_consult)
        r = requests.get(url_consult,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})

        encounter_details = json.loads(r.content)
        print(encounter_details)
        print(type(encounter_details))
            #under visit fetch episode, encounter and other details required

        #when a doctor clicks on an encounter the doctor is redirected to the encounter details page in the consultation application
            #view opd_consultation

        context['encounter_details'] = json.loads(encounter_details)
        context['doctor_details'] = doctor_details
        context['length'] = len(context['encounter_details'])
        context['user'] = data
        return render(request, 'access_frontend/doctor_profile.html', context)

@jwt_token_required
def nurse_profile(request,data,status):
    if status!=200:
        return redirect(login)

    else:

        #request.session['tenantID'] - will give facility id
        #get facility details
        facilityId=data['extra']['facilityId'][0]['uniqueFacilityIdentificationNumber']
        facility_details = 0
        #get doctor user details (how do we get dId)

        content={}
        values = dict(content)
        values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
        values['userId']=request.session['userId']
        values['userGroup']=request.session['userGroup']
        values['facilityTypeCode']=request.session['facilityTypeCode']
        payload = json.dumps(values)



        context = {}
        dId = data['username']
        url = settings.HDIS_DOCTOR_ADMINISTRATION + "/api/doctor_provider_details/" + dId

        access_token = request.session.get('access_token')
        r = requests.get(url,data=payload,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})

        a = r.content.decode('utf-8')
        doctor_details = json.loads(a)
        print(doctor_details)
        #get visit details for the facility+doctor+date (give option to select date and update the list of visits
        date = datetime.now().strftime("%Y-%m-%d")
        url_consult = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective/" + doctor_details['facilityId']['uniqueFacilityIdentificationNumber'] + "/" + doctor_details['uniqueIndividualHealthCareProviderNumber'] + "/" + date
        print(url_consult)
        r = requests.get(url_consult,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})

        encounter_details = json.loads(r.content)
        print(encounter_details)
        print(type(encounter_details))
            #under visit fetch episode, encounter and other details required

        #when a doctor clicks on an encounter the doctor is redirected to the encounter details page in the consultation application
            #view opd_consultation

        context['encounter_details'] = json.loads(encounter_details)
        context['doctor_details'] = doctor_details
        context['length'] = len(context['encounter_details'])
        context['user'] = data
        return render(request, 'access_frontend/nurse_profile.html', context)

def getfacilityType(code):
    url = settings.HDIS_ORG_MASTER+"/get_facilitytypename?ftype="+code
    r = requests.get(url,headers={'Content-type': 'application/json', 'Accept': 'application/json'})

    a = r.content.decode('utf-8')
    b=json.loads(a)
    print(b[0])
    print (b[0]['facility_type_description'])
    return b[0]['facility_type_description']

def superadmin(request):
    value = request.COOKIES.get('x-access-token')

    url = settings.HDIS_AUTH_SERVER+"/getfacilitydetails"
    r = requests.get(url,headers={'Content-type': 'application/json', 'Accept': 'application/json','x-access-token':value})

    a = r.content.decode('utf-8')
    facilities=[]
    
    indata=json.loads(a)
    print(indata['users'])

    for facility in indata['users'] :
        if facility['count']>0 :
            thisfacility={}
            facilityname=getfacilityType(facility['ftype'])
            print(facilityname)
            thisfacility['fname']=facilityname
            thisfacility['fcount']=facility['count']
            facilities.append(thisfacility)

    print(facilities)

    url = settings.HDIS_AUTH_SERVER+"/getfacilityusers"
    r = requests.get(url,headers={'Content-type': 'application/json', 'Accept': 'application/json','x-access-token':value})

    a = r.content.decode('utf-8')

    userdata=json.loads(a)
    print(userdata['users'])
   


    context={'facility':facilities,'users':userdata['users']}

    return render(request, 'access_frontend/master_admin.html',context)


@jwt_token_required
def dashboard(request,data,status):

    print(status)
    print(data)
    if status==200:
        if any(d['name'] == 'Super' for d in data['groups']):
            return redirect(superadmin)
        elif any(d['name'] == 'Doctor' for d in data['groups']):
            #fetch providerID and save in cookie
            return redirect(doctor_profile)
        elif any(d['name'] == 'Front Desk' for d in data['groups']):
            #fetch providerID and save in cookie
            return redirect(front_desk_home)
        else: 
            context={'user':data}
            return render(request, 'access_frontend/homedash.html', context)
    else:
        return redirect(login)

     





def logout(request):

    response=redirect(login)
    response.set_cookie('x-access-token','')
    tenandID = request.session.get('tenantID')
    if tenandID is not None:
        del request.session['tenantID']

    return response


def home(request):
    return render(request, 'access_frontend/select_services.html')    

def select_microservices(request):
    return render(request, 'access_frontend/select_microservices.html')  

def register_facility(request):    

    if request.method == 'POST':

        
        url = settings.HDIS_ORG_MASTER+"/facility_management/facility/"
       
       # form = FacilityRegisterForm(request.POST)
       # if form.is_valid():
       #     serialized_data = serialize('json', [form.cleaned_data])
       #     print(serialized_data)
       # else:
       #     print(form.errors.as_data)    
        
        values = dict(request.POST.items())
        payload = json.dumps(values)
        print (payload)
        
        r = requests.post(url, data=payload,
                            headers={'Content-type': 'application/json', 'Accept': 'application/json'})

        a = r.content.decode('utf-8')

        
        if r.status_code==201:
            data=json.loads(a)
            print(data)


            request.session['access_token'] = data['access']
            request.session['refresh_token'] = data['refresh']
            
            #values=json.loads(a)
            token='123'
            next='facilityusers'
            


            response= redirect(setpassword,token,next)
            print('token is')
            print(request.session['access_token'] )
            #response.set_cookie('x-access-token',r.headers["JWToken"])
            return response
        else:
            url = settings.HDIS_ORG_MASTER+"/facility_management/facilitytype/"
            r = requests.get(url,headers={'Content-type': 'application/json', 'Accept': 'application/json'})

            a = r.content.decode('utf-8')
            messages=[]
            form=FacilityRegisterForm(initial={'facilityInternalClass': 1})
            data=json.loads(a)
            print(data)
            choices = [(item['facility_type_code'], item['facility_type_description']) for item in data]
            form.fields['facilityTypeCode'].choices=choices     


            messages.append('Error :Error Registering, email already exists')
            context={'data':json.loads(a),'messages':messages,'form':form}
            return render(request, 'access_frontend/register_facility.html',context)


    else:

        url = settings.HDIS_ORG_MASTER+"/facility_management/facilitytype/"
        r = requests.get(url,headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        form=FacilityRegisterForm(initial={'facilityInternalClass': 1})
        

        a = r.content.decode('utf-8')

        data=json.loads(a)
        print(data)
        choices = [(item['facility_type_code'], item['facility_type_description']) for item in data]
        form.fields['facilityTypeCode'].choices=choices       
        context={'form':form}
        return render(request, 'access_frontend/register_facility.html',context)


def setpassword(request,token,next):

    user={"is_authenticated":False}
    context={'user':user,'token':token,'next':next}

    return render(request, 'access_frontend/set_password.html',context)

@jwt_token_required
def facilityusers(request,data,status):

   # value = request.COOKIES.get('x-access-token')
   # if value is None:
   #     return redirect(login)
   # else:
   #     print(value)

    #url = settings.HDIS_AUTH_SERVER+"/getusers"
    print("getting users")
    url=settings.HDIS_ORG_MASTER+"/facility_management/facility/"
    content = {}
    content['userId']=request.session['userId']
    content['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
    values = dict(content)
    payload = json.dumps(values)
    access_token = request.session.get('access_token')
    r = requests.get(url, data=payload,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})

    a = r.content.decode('utf-8')
    print(r.status_code)

    if r.status_code==200:
        values=json.loads(a)
        print(values)
        user=values['facility']
        users=values['users'][0]['memberId']
        facility=values['users'][0]['facilityId']
        user["is_authenticated"]=True #user is logged in
        context={'user':user,'users':users,'facility':facility}

        return render(request, 'access_frontend/facilityusers.html',context)

    else:
        return redirect(login)



def changepassword(request):


    print(request)
    #url = settings.HDIS_AUTH_SERVER+"/setpassword"
    url=url = settings.HDIS_AUTH_SERVER+"/access/setpassword/"
    content = {"password":request.POST.get("password"),
    "confirm_password":request.POST.get("confirm_password"),
    "token":request.POST.get("token")

    }
    values = dict(content)
    payload = json.dumps(values)
    print(payload)
    access_token = request.session.get('access_token')
    print(access_token)
    r = requests.post(url, data=payload,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})

    a = r.content.decode('utf-8')
    print(a)

    if r.status_code==200:
        #if request.POST.get("next")=='facilityusers':
        return redirect(facilityusers)
    else:
        return redirect(login)
        

@jwt_token_required
def getuserdetails(request,uId,data,status):
    print('check get user details')
    url = settings.HDIS_ORG_MASTER+"/facility_management/facilityuser/"+uId
    content = {}
    values = dict(content)
    values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
    values['userId']=request.session['userId']
    values['userGroup']=request.session['userGroup']
    values['facilityTypeCode']=request.session['facilityTypeCode']
    payload = json.dumps(values)
    print(payload)
    access_token = request.session.get('access_token')
    r = requests.get(url, data=payload,
                    headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})

    a = r.content.decode('utf-8')
    print(r.status_code)
    

    if r.status_code==200:   

        user=json.loads(a)
        print(user)
        user["is_authenticated"]=True
        if user['userRole']=='Doctor':
            url = settings.HDIS_DOCTOR_ADMINISTRATION + "/api/doctors_detail/" + uId
            access_token = request.session.get('access_token')
            r = requests.get(url, data=payload,
                    headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
            print(r.content.decode('utf-8'))
            doctor_details=json.loads(r.content.decode('utf-8'))
            user['doctorRegistrationNumber']=doctor_details['personal']['doctorRegistrationNumber']
            user['doctorSpeciality']=doctor_details['doctor']['doctorSpeciality']
            user['doctorBankDetails']=doctor_details['doctor']['doctorBankDetails']
            user['languagesKnown']=doctor_details['personal']['languagesKnown']
            user['currentCity']=doctor_details['personal']['currentCity']

            doctor_documents=doctor_details['documents']
            base_document_url=settings.HDIS_DOCTOR_ADMINISTRATION
            form=FacilityEditDoctorForm(initial=user)
            
            specialities=SpecialityType.objects.all()
            choices = [(speciality.Medical_Specialty_Type_Name, speciality.Medical_Specialty_Type_Name) for speciality in specialities]

            form.fields['doctorSpeciality'].choices=choices  
            #form.fields['doctorSpeciality'].initial=   user['doctorSpeciality']


            context={'user':user,'facility':data['extra']['facilityId'][0],'admin':data,'form':form,'doctor_documents':doctor_documents,'base_document_url':base_document_url}

        else:    
            form=FacilityEditUserForm(initial=user)
            context={'user':user,'facility':data['extra']['facilityId'][0],'admin':data,'form':form}

          
        return render(request, 'access_frontend/edituser.html',context)
    elif r.status_code==403:
        return redirect(login)

def edituser(request):

    
    if request.POST.get("userRole")=="Doctor":
        form=FacilityEditDoctorForm(request.POST,request.FILES)
        specialities=SpecialityType.objects.all()
        choices = [(speciality.Medical_Specialty_Type_Name, speciality.Medical_Specialty_Type_Name) for speciality in specialities]
        print(choices)

        form.fields['doctorSpeciality'].choices=choices  
    else:
        form=FacilityEditUserForm(request.POST)

        

    if form.is_valid():
          print('form is valid')
    else:
          print(form.errors.as_data)   


    id=request.POST.get("memberId")
    url = settings.HDIS_ORG_MASTER+"/facility_management/facilityuser/"+id

    content = {"password":request.POST.get("password"),
    "confirm_password":request.POST.get("confirm_password"),
    "email":request.POST.get("memberEmail"),
    "mobile":request.POST.get("memberMobile"),
    "name":request.POST.get("memberName"),
    "userid":request.POST.get("memberId")
    

    }
    values = dict(content)
    values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
    values['userId']=request.session['userId']
    values['userGroup']=request.session['userGroup']
    values['facilityTypeCode']=request.session['facilityTypeCode']
    values['doctorRegistrationNumber']=request.POST.get("doctorRegistrationNumber")
    
    values['doctorSpeciality']=request.POST.get("doctorSpeciality")
    values['currentCity']=request.POST.get("currentCity")
    values['languagesKnown']=request.POST.get("languagesKnown")
    values['doctorBankDetails']=request.POST.get("doctorBankDetails")


    payload = json.dumps(values)
    print(payload)
    access_token = request.session.get('access_token')
    r = requests.put(url, data=payload,
                    headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})

    a = r.content.decode('utf-8')
    print(r.status_code)

    if r.status_code==201:
        if request.POST.get("userRole")=="Doctor":
            url = settings.HDIS_DOCTOR_ADMINISTRATION + "/api/doctors_detail/" + id
            access_token = request.session.get('access_token')
            files={}
            try:
                doctorRegistrationCertificate=request.FILES['doctorRegistrationCertificate']
                files['doctorRegistrationCertificate']=doctorRegistrationCertificate
            except MultiValueDictKeyError:
                print('no registration cert')

            try:
                doctorSignatures=request.FILES['doctorSignatures']
                files['doctorSignatures']=doctorSignatures
            except MultiValueDictKeyError:
                print('no registration cert')     





            
            print(files)
            r = requests.post(url,data=values,files=files,
                            headers={'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
            
            a = r.content.decode('utf-8')
            print(r.status_code)
        
        return redirect(facilityusers)



def bulkupload(request):

    if request.method == 'POST':
        value = request.COOKIES.get('x-access-token')
        if value is None:
            return redirect(login)

        else:
            url = settings.HDIS_ORG_MASTER+"/adduser"         
            content = {"user_name":request.POST.get("user_name"),
            "user_email":request.POST.get("user_email"),
            "user_type":request.POST.get("user_type")

            }
            values = dict(content)
            payload = json.dumps(values)
            print(payload)
            r = requests.post(url, data=payload,
                                headers={'Content-type': 'application/json', 'Accept': 'application/json','x-access-token':value})

            a = r.content.decode('utf-8')
            print(r.status_code)

            return redirect(facilityusers)

    else:

        tenandID = request.session.get('tenantID')
     
        if tenandID is None:

            value = request.COOKIES.get('x-access-token')
            if value is None:
                return redirect(login)

            else:
                print(value)

            url = settings.HDIS_AUTH_SERVER+"/access"
            content = {"test":"this"}
            values = dict(content)
            payload = json.dumps(values)
            r = requests.post(url, data=payload,
                                headers={'Content-type': 'application/json', 'Accept': 'application/json','x-access-token':value})

            a = r.content.decode('utf-8')
            print(r.status_code)
            if r.status_code==200:
                user=json.loads(a)
                print(user)
                request.session['tenantID']=user['tenantID']
                request.session['userid']=user['userid']
                request.session['role']=user['role']
                user["is_authenticated"]=True
                authenticated=True
                context={'user':user}

            else:
                user={"is_authenticated":False}
                authenticated=False
                context={'user':user}

                #return render(request, 'doctor_administration/register.html',context)
            if authenticated==True :
                return render(request, 'access_frontend/bulkupload.html',context)
            else:
                return redirect(login)

        else:
            print('user is authenticated')
            user={"is_authenticated":True,"role":request.session["role"]}
            authenticated=True
            context={'user':user}
            return render(request, 'access_frontend/bulkupload.html',context)


@jwt_token_required
def front_desk_home(request,data,status):
    context={'user':data}
    return render(request, 'access_frontend/front_desk_dash.html',context)

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
            values={}
            values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
            values['userId']=request.session['userId']
            values['userGroup']=request.session['userGroup']
            values['facilityTypeCode']=request.session['facilityTypeCode']
            payload = json.dumps(values)



            context = {}
            url = settings.HDIS_PATIENT_REGISTRATION+"/api/patients/uhid/" + str(uhid)

            access_token = request.session.get('access_token')
            r = requests.get(url,data=payload,
                            headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
            
            
            
            if r.status_code==200:
                patient_list = json.loads(r.content.decode('utf-8'))
                par=json.loads(patient_list) # not sure why json.loads needs to be called twice
                context = {'user': data, 'patient_list': par}
                return render(request, 'appointment_booking/select_patient.html', context)
            else:
                messages=[]
                messages.append('Error :No Patient Found')
                context={'user':data,'messages':messages}
                return render(request, 'appointment_booking/search_patient.html', context)

@jwt_token_required
def search_patient_demo(request,data,status):
    if status!=200:
        return redirect(login) 
    else: 
        if request.method == 'GET':
            context={"user":data}
            return render(request, 'appointment_booking/search_patient.html', context)
        else:
            values = dict(request.POST.items())
            values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
            values['userId']=request.session['userId']
            values['userGroup']=request.session['userGroup']
            values['facilityTypeCode']=request.session['facilityTypeCode']
            values['mode']='demo'
            payload = json.dumps(values)



            url = settings.HDIS_PATIENT_REGISTRATION+"/api/patients/search/"

            access_token = request.session.get('access_token')
            r = requests.post(url,data=payload,
                            headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
            
            
            if r.status_code==200:
                patient_list = json.loads(r.content.decode('utf-8'))
                par=json.loads(patient_list) # not sure why json.loads needs to be called twice
                context = {'user': data, 'patient_list': par}
                return render(request, 'appointment_booking/select_patient.html', context)
            else:
                messages=[]
                messages.append('Error :No Patient Found')
                context={'user':data,'messages':messages}
                return render(request, 'appointment_booking/search_patient.html', context)

@jwt_token_required
def search_patient_mobile(request,data,status):
        values = dict(request.POST.items())
        values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
        values['userId']=request.session['userId']
        values['userGroup']=request.session['userGroup']
        values['facilityTypeCode']=request.session['facilityTypeCode']
        values['mode']='mobile'
        payload = json.dumps(values)



        url = settings.HDIS_PATIENT_REGISTRATION+"/api/patients/search/"

        access_token = request.session.get('access_token')
        r = requests.post(url,data=payload,
                        headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})
        
        
        
        #print('user is authenticated')
        if r.status_code==200:
            patient_list = json.loads(r.content.decode('utf-8'))
            par=json.loads(patient_list) # not sure why json.loads needs to be called twice
            context = {'user': data, 'patient_list': par}
            return render(request, 'appointment_booking/select_patient.html', context)
        else:
            messages=[]
            messages.append('Error :No Patient Found')
            context={'user':data,'messages':messages}
            return render(request, 'appointment_booking/search_patient.html', context)


@jwt_token_required
def adduser(request,data,status):
    if request.method == 'POST':
    
        url = settings.HDIS_ORG_MASTER+"/facility_management/facilityuser/"
       
        values = dict(request.POST.items())
        values['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
        values['userId']=request.session['userId']
        values['userGroup']=request.session['userGroup']
        values['facilityTypeCode']=request.session['facilityTypeCode']
        payload = json.dumps(values)
        print (payload)

 
        access_token = request.session.get('access_token')
        r = requests.post(url, data=payload,
                    headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})

        a = r.content.decode('utf-8')
        retData=json.loads(a)
        print(retData)
        print(r.status_code)
        if request.POST['usertType']=="Doctor":

            return redirect(getuserdetails,uId=retData['created'])
        else:
            return redirect(facilityusers)

    else:

       if status==200:
            
            access_token = request.session.get('access_token')
            url = settings.HDIS_ORG_MASTER+"/facility_management/facilityusertypes/"
            content={}
            content['userId']=request.session['userId']
            content['uniqueFacilityIdentificationNumber']=request.session['uniqueFacilityIdentificationNumber']
            content['facilityTypeCode']=request.session['facilityTypeCode']
            values = dict(content)
            payload = json.dumps(values)
            r = requests.get(url,data=payload,headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {access_token}'})

            a=json.loads(r.content.decode('utf-8'))
            userTypes=json.loads(a)
            print(userTypes)
            form=FacilityAddUserForm()
        

            a = r.content.decode('utf-8')

            for item in userTypes:
                print(item)
            choices = [(item, item) for item in userTypes]
            form.fields['usertType'].choices=choices       
            context={'form':form}





            user={"is_authenticated":True}
            authenticated=True
            context={'user':user,'form':form}
            return render(request, 'access_frontend/adduser.html',context)
       else:
           return redirect(login)







        





