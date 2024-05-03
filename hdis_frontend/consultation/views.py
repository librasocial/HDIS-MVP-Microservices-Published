from django.shortcuts import render
import re
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
import requests
import json
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from datetime import datetime, timezone, date, timedelta
import random
from django.contrib.auth import login
import hashlib
import urllib.parse
import os
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import messages
import smtplib
from django.template import Context, Template
from django.template.loader import get_template
from django.core.files.base import ContentFile
import base64
#from letsdoc.settings.base import MEDIA_ROOT, MEDIA_URL
import time
import tempfile
from django.core.files.base import File
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q
from django.contrib.sessions.models import Session
import logging
import math
from calendar import monthrange
import ast
import socket
from access_frontend.views import login, doctor_profile
from django.conf import settings
from hdis_frontend.decorators import jwt_token_required

def get_encounter_details(eId,prId,access_token):
    url_consult = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective/" + eId + "/" + prId
    print(url_consult)
    r = requests.get(url_consult, headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
    encounter_details = json.loads(json.loads(r.content))
    print(encounter_details)
    url_consult = settings.HDIS_CONSULTATION_OBJECTIVE + "/api/consultationObjective/" + eId + "/" + prId
    print(url_consult)
    r = requests.get(url_consult, headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
    encounter_details.update(json.loads(json.loads(r.content)))
    print(encounter_details)
    url_consult = settings.HDIS_CONSULTATION_ASSESSMENT + "/api/consultationAssessment/" + eId + "/" + prId
    print(url_consult)
    r = requests.get(url_consult, headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
    encounter_details.update(json.loads(json.loads(r.content)))
    print(encounter_details)
    url_consult = settings.HDIS_CONSULTATION_PLAN + "/api/consultationPlan/" + eId + "/" + prId
    print(url_consult)
    r = requests.get(url_consult, headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
    encounter_details.update(json.loads(json.loads(r.content)))
    print(encounter_details)
    return(encounter_details)
@jwt_token_required
def opd_consultation(request,data,status):
    access_token = request.session.get('access_token')
    if access_token is None:
        return redirect(login)

    else:
        if request.method == 'POST':

            print(access_token)
            content = list(request.POST.items())
            values = dict(content)
            eId = values['eId']
            prId = values['prId']

            if 'video_call' in request.POST:
                vc = 1
                order_id = values['request_id']
                encounter_details = encounterDetails.objects.get(encounterId=order_id)
                status_encounter = encounter_status.objects.get(order_id=order_id)
                status_encounter.video_status = vc
                status_encounter.save()
                case_status = encounter_status.objects.get(encounter_id=encounter_details)
                patient_details = Patient.objects.get(ProvidersPatientID=encounter_details.patientId)
                patient_name = patient_details.PatientName
                patient_mobile = patient_details.patientMobileNumber
                patient_email = patient_details.patientEmailAddressURL
                room_url = status_encounter.encounter_video_link + '&name=' + provider_details.providerName + "&password=" + encounter_details.encounterId
                video_link = "https://" + request.META['HTTP_HOST'] + "/doctor_consultation/" + str(
                    encounter_details.encounter_uid) + "/encounter_consultation/"
                doctor_name = status_encounter.case_assigned_to.providerName
                # Email
                template = get_template("doctor_consultation\\video_consultation.html")
                context = {'patient_name': patient_name, 'patient_email': patient_email, 'video_link': video_link,
                           'doctor_name': doctor_name}
                email_body = template.render(context)
                # email_body = render_to_string(template, context)
                text_email = strip_tags(email_body)
                email_send = EmailMultiAlternatives('LetsDoc: Video Consultation Link', text_email,
                                                    to=[patient_email, "support@letsdoc.in"])
                email_send.attach_alternative(email_body, "text/html")
                email_send.send()
                # Hi {#var#}{#var#}It was a pleasure talking to you on the phone.{#var#}Please Click on the like {#var#} to initiate the video consultation. Thanks for using LetsDoc.
                msg_encode = "Hi " + patient_name + "\nPlease Click on the link " + video_link + " to join the video consultation with your doctor. Thanks for using LetsDoc."
                # sms_msg = urllib.parse.quote(msg_encode)
                sms_msg = msg_encode
                payload = {}
                payload['userId'] = sms_user_id_trans
                payload['appid'] = "lhtalt"
                payload['pass'] = sms_pswd_trans
                payload['contenttype'] = "1"
                payload['from'] = "LTSDOC"
                payload['to'] = "91" + patient_mobile
                payload['selfid'] = "true"
                payload['intflag'] = "false"
                payload['text'] = sms_msg
                payload['s'] = "1"
                payload['alert'] = "1"
                payload['dpi'] = "1201159523893139905"
                payload['dtm'] = "1007163280523479312"
                payload['tc'] = "3"
                data = json.dumps(payload)
                b = request_dump(dump=data, source='sms_request')
                b.save()
                headers = {}
                headers['Content-type'] = "application/json"
                # r = requests.post(url_sms, data = json.dumps(payload),headers={'Content-type': 'application/json'})
                r = requests.request("POST", url_sms, data=data, headers=headers)
                k = r.content
                a = (r.text + str(k) + str(r.status_code))
                b = request_dump(dump=a, source='sms_response')
                b.save()
                # WhatsApp
                message_payload = {}
                message_payload['messages'] = []
                message_details = {}
                message_details['sender'] = sender
                message_details['to'] = "91" + patient_mobile
                message_details['channel'] = "wa"
                message_details['type'] = 'template'
                message_details['template'] = {}
                message_details['template']['body'] = []
                template_body = {}
                template_body["type"] = "text"
                template_body['text'] = patient_name
                message_details['template']['body'].append(template_body)
                template_body = {}
                template_body["type"] = "text"
                template_body['text'] = video_link
                message_details['template']['body'].append(template_body)
                message_details['template']['templateId'] = '1007163280523479312'
                message_details['template']['langCode'] = "en"
                message_payload['messages'].append(message_details)
                message_payload['responseType'] = 'json'
                message_url = whatsapp_message_url
                headers = {}
                headers['Content-type'] = "application/json"
                headers['user'] = test_entreprise_id
                headers['pass'] = sender_pass
                headers['Sender'] = sender
                r = requests.request("POST", message_url, data=json.dumps(message_payload), headers=headers)
                k = r.content
                a = json.dumps(message_payload) + (r.text + str(k) + str(r.status_code))
                b = request_dump(dump=a, source='whatsapp_doctor_update')
                b.save()
                new_case_dict = assign_same_encounter(order_id, provider_details)
                return render(request, 'doctor_consultation/facility_consultation.html',
                              {'template_name': template_name, 'vc': vc, 'encounter_details': new_case_dict,
                               'room_url': room_url})
            elif 'audio_call' in request.POST:
                auth_key = knowlarity_auth_key
                # sr_cli = randint(0,2)
                sr_number = '+917348954851'
                cli_number = '+918068122055'
                # cli_number = '+918048767361'
                url = knowlarity_url
                provider_number = provider_details.providerMobile
                order_id = values['request_id']
                payload = {}
                payload['patient_number'] = "+91" + values['patient_number']
                payload['request_id'] = values['request_id']
                payload['sr_number'] = sr_number
                payload['cli_number'] = cli_number
                payload['doctor_number'] = '+91' + provider_number
                headers = {}
                # headers['Content-type'] = 'multipart/form-data'
                # headers['Accept'] = 'application/json'
                headers['auth_key'] = auth_key
                r = requests.request("POST", url, data=payload, headers=headers)
                k = r.content
                a = (r.text + str(k) + str(r.status_code))
                b = request_dump(dump=a, source='knowlarity_encounter_test')
                b.save()
                # r = requests.post(url, data = json.dumps(payload), headers = headers)
                messages.add_message(request, messages.SUCCESS, 'Call initiated successfully')
                new_case_dict = assign_same_encounter(order_id, provider_details)
                return render(request, 'doctor_consultation/facility_consultation.html',
                              {'template_name': template_name, 'vc': vc, 'encounter_details': new_case_dict})
            elif 'update_status' in request.POST:
                reschedule_reason = values['reschedule_reason']
                encounter_id = values['order_id']
                order_status = encounter_status.objects.get(order_id=encounter_id)
                if int(reschedule_reason.split(":")[0]) < 5:
                    order_status.order_status = 3
                    # order_status.episodeStatusId = episodeStatus.objects.get(episodeStatusCode = '3')
                else:
                    order_status.order_status = 4
                    order_status.episodeStatusId = episodeStatus.objects.get(episodeStatusCode='4')
                order_status.last_status_update_date = datetime.now(timezone.utc) + timedelta(seconds=(5 * 3600) + 1800)
                order_status.number_of_modifies += 1
                order_status.save()
                order_modified = encounter_modified(encounter_id=order_status.encounter_id, order_id=encounter_id,
                                                    modified_time=datetime.now(timezone.utc) + timedelta(
                                                        seconds=(5 * 3600) + 1800), type_of_change=reschedule_reason,
                                                    modified_by=provider_details.id)
                order_modified.save()
                encounter_retry_update()
                provider_login_check()
                new_case_dict = assign_encounter(provider_email)
                return render(request, 'doctor_consultation/facility_consultation.html',
                              {'template_name': template_name, 'vc': vc, 'encounter_details': new_case_dict})
            elif 'vitalSigns' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_OBJECTIVE + "/api/consultationObjective"
                print(url)
                print(values)
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})
            elif 'familyHistory' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective"
                print(url)
                values['familyMemberRelationship_list'] = request.POST.getlist('familyMemberRelationship')
                values['familyMemeberHealthCondition_list'] = request.POST.getlist('familyMemeberHealthCondition')
                values['familyMemberHealthConditionStatus_list'] = request.POST.getlist('familyMemberHealthConditionStatus')
                values['familyMemeberAgeAtOnset_list'] = request.POST.getlist('familyMemeberAgeAtOnset')
                values['causeOfDeathKnown_list'] = request.POST.getlist('causeOfDeathKnown')
                values['familyMemeberAgeAtDeath_list'] = request.POST.getlist('familyMemeberAgeAtDeath')
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})
            elif 'patientComorbidities' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective"
                print(url)
                values['comorbidityHealthCondition_list'] = request.POST.getlist('comorbidityHealthCondition')
                values['comorbidityHealthConditionStatus_list'] = request.POST.getlist('comorbidityHealthConditionStatus')
                values['ageAtOnsetOfHealthCondition_list'] = request.POST.getlist('ageAtOnsetOfHealthCondition')
                values['procedurePerformed_list'] = request.POST.getlist('procedurePerformed')
                values['patientDispositionAfterProcedure_list'] = request.POST.getlist('patientDispositionAfterProcedure')
                values['procedureDate_list'] = request.POST.getlist('procedureDate')
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})
            elif 'socialHistory' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective"
                print(url)
                values['habitDescription_list'] = request.POST.getlist('habitDescription')
                values['currentStatus_list'] = request.POST.getlist('currentStatus')
                values['habitType_list'] = request.POST.getlist('habitType')
                values['smokingFreqency_list'] = request.POST.getlist('smokingFreqency')
                values['alcoholIntakeFrequency_list'] = request.POST.getlist('alcoholIntakeFrequency')
                values['onsetSince_list'] = request.POST.getlist('onsetSince')
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})
            elif 'complications' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective"
                print(url)
                values['complicationType_list'] = request.POST.getlist('complicationType')
                values['complicationName_list'] = request.POST.getlist('complicationName')
                values['complicationDescription_list'] = request.POST.getlist('complicationDescription')
                values['complicationDate_list'] = request.POST.getlist('complicationDate')
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})
            elif 'disability' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective"
                print(url)
                values['disabilityType_list'] = request.POST.getlist('disabilityType')
                values['disabilityName_list'] = request.POST.getlist('disabilityName')
                values['disabilityDescription_list'] = request.POST.getlist('disabilityDescription')
                values['disabilityDate_list'] = request.POST.getlist('disabilityDate')
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})
            elif 'relapse' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective"
                print(url)
                values['relapseType_list'] = request.POST.getlist('relapseType')
                values['relapseName_list'] = request.POST.getlist('relapseName')
                values['relapseDescription_list'] = request.POST.getlist('relapseDescription')
                values['relapseDate_list'] = request.POST.getlist('relapseDate')
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})
            elif 'remission' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective"
                print(url)
                values['remissionType_list'] = request.POST.getlist('remissionType')
                values['remissionName_list'] = request.POST.getlist('remissionName')
                values['remissionDescription_list'] = request.POST.getlist('remissionDescription')
                values['remissionDate_list'] = request.POST.getlist('remissionDate')
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})
            elif 'allergy' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective"
                print(url)
                values['allergyProduceDescription_list'] = request.POST.getlist('allergyProduceDescription')
                values['allergyReactionName_list'] = request.POST.getlist('allergyReactionName')
                values['allergyRectionDescription_list'] = request.POST.getlist('allergyRectionDescription')
                values['allergySeverityDescription_list'] = request.POST.getlist('allergySeverityDescription')
                values['allergyStatus_list'] = request.POST.getlist('allergyStatus')
                values['allergyEventType_list'] = request.POST.getlist('allergyEventType')
                values['allergyHistory_list'] = request.POST.getlist('allergyHistory')
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})
            elif 'chiefComplaints' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_SUBJECTIVE + "/api/consultationSubjective"
                print(url)
                values['chiefComplaintName_list'] = request.POST.getlist('chiefComplaintName')
                values['chiefComplaintBodySite_list'] = request.POST.getlist('chiefComplaintBodySite')
                values['chiefComplaintDuration_list'] = request.POST.getlist('chiefComplaintDuration')
                values['chiefComplaintDurationUnit_list'] = request.POST.getlist('chiefComplaintDurationUnit')
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})

            elif 'examination' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_ASSESSMENT + "/api/consultationAssessment"
                print(url)
                values['examinationSystem_list'] = request.POST.getlist('examinationSystem')
                values['examinationType_list'] = request.POST.getlist('examinationType')
                values['bodySiteName_list'] = request.POST.getlist('bodySiteName')
                values['examinationFinding_list'] = request.POST.getlist('examinationFinding')
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})
            elif 'diagnosis' in request.POST:
                access_token = request.session.get('access_token')
                url = settings.HDIS_CONSULTATION_ASSESSMENT + "/api/consultationAssessment"
                print(url)
                values['healthConditionType_list'] = request.POST.getlist('healthConditionType')
                values['healthConditionName_list'] = request.POST.getlist('healthConditionName')
                values['healthConditionDescription_list'] = request.POST.getlist('healthConditionDescription')
                values['healthConditionCategory_list'] = request.POST.getlist('healthConditionCategory')
                values['healthConditionStatus_list'] = request.POST.getlist('healthConditionStatus')
                values['diagnosisPriority_list'] = request.POST.getlist('diagnosisPriority')
                values['presentHealthConditionOnsetDate_list'] = request.POST.getlist('presentHealthConditionOnsetDate')
                payload = json.dumps(values)
                r = requests.post(url, data=payload,
                                  headers={'Content-type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': f'Bearer {access_token}'})
                encounter_details = get_encounter_details(eId, prId, access_token)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details': encounter_details})
            elif 'save_consultation_notes' in request.POST:
                encounter_details = encounterDetails.objects.get(encounterId=values['request_id'])
                case_status = encounter_status.objects.get(encounter_id=encounter_details)
                patient_details = Patient.objects.get(ProvidersPatientID=encounter_details.patientId)
                saving_date = datetime.now(timezone.utc) + timedelta(seconds=(5 * 3600) + 1800)
                encounter_notes_document = {}
                prescription_id = files_created_during_encounter(encounter_id=encounter_details,
                                                                 order_id=encounter_details.encounterId,
                                                                 file_date=datetime.now(timezone.utc) + timedelta(
                                                                     seconds=(5 * 3600) + 1800))
                prescription_id.save()
                if 'dob' in request.POST:
                    patient_dob = values['dob']
                    date_dob = datetime.strptime(patient_dob, "%Y-%m-%d").date()
                    dob_year = str(datetime.now().year - date_dob.year)
                    dob_month = str(datetime.now().month - date_dob.month)
                    dob_day = str(datetime.now().day - date_dob.day)
                    patient_age = dob_year + ',' + dob_month + ',' + dob_day
                    patient_details.patientAge = patient_age
                    patient_details.patientDOB = date_dob
                    patient_details.save()



                if 'patient_gender' in request.POST:
                    patient_gender = values['patient_gender']
                    patient_details.patientGender = patient_gender
                    patient_details.save()
                if 'body_height' in request.POST:
                    if values['body_height'] != '':
                        vitalTypeCode = vitalSignsResultType.objects.get(vitalSignsResultTypeName='Body Height')
                        vitalStatus = vitalSignsResultStatus.objects.get(vitalSignsResultStatusCode='2')
                        vitalSignResultUnit = unitOfMeasurement.objects.get(unitOfMeasurementShortName='Cm')
                        patient_height = patientVitals(encounterId=encounter_details, vitalTypeCode=vitalTypeCode,
                                                       vitalStatus=vitalStatus,
                                                       vitalSignResultValue=str(values['body_height']),
                                                       vitalSignResultUnit=vitalSignResultUnit)
                        patient_height.save()
                if 'body_weight' in request.POST:
                    if values['body_weight'] != '':
                        vitalTypeCode = vitalSignsResultType.objects.get(vitalSignsResultTypeName='Body Weight')
                        vitalStatus = vitalSignsResultStatus.objects.get(vitalSignsResultStatusCode='2')
                        vitalSignResultUnit = unitOfMeasurement.objects.get(unitOfMeasurementShortName='Kg')
                        body_weight = patientVitals(encounterId=encounter_details, vitalTypeCode=vitalTypeCode,
                                                    vitalStatus=vitalStatus,
                                                    vitalSignResultValue=str(values['body_weight']),
                                                    vitalSignResultUnit=vitalSignResultUnit)
                        body_weight.save()
                if 'systolic' in request.POST:
                    if values['systolic'] != '':
                        vitalTypeCode = vitalSignsResultType.objects.get(vitalSignsResultTypeName='Systolic Blood Pressure')
                        vitalStatus = vitalSignsResultStatus.objects.get(vitalSignsResultStatusCode='2')
                        vitalSignResultUnit = unitOfMeasurement.objects.get(unitOfMeasurementShortName='Mmhg')
                        systolic = patientVitals(encounterId=encounter_details, vitalTypeCode=vitalTypeCode,
                                                 vitalStatus=vitalStatus, vitalSignResultValue=str(values['systolic']),
                                                 vitalSignResultUnit=vitalSignResultUnit)
                        systolic.save()
                if 'diastolic' in request.POST:
                    if values['diastolic'] != '':
                        vitalTypeCode = vitalSignsResultType.objects.get(
                            vitalSignsResultTypeName='Diastolic Blood Pressure')
                        vitalStatus = vitalSignsResultStatus.objects.get(vitalSignsResultStatusCode='2')
                        vitalSignResultUnit = unitOfMeasurement.objects.get(unitOfMeasurementShortName='Mmhg')
                        diastolic = patientVitals(encounterId=encounter_details, vitalTypeCode=vitalTypeCode,
                                                  vitalStatus=vitalStatus, vitalSignResultValue=str(values['diastolic']),
                                                  vitalSignResultUnit=vitalSignResultUnit)
                        diastolic.save()
                if 'body_temperature' in request.POST:
                    if values['body_temperature'] != '':
                        vitalTypeCode = vitalSignsResultType.objects.get(vitalSignsResultTypeName='Temperature')
                        vitalStatus = vitalSignsResultStatus.objects.get(vitalSignsResultStatusCode='2')
                        vitalSignResultUnit = unitOfMeasurement.objects.get(unitOfMeasurementShortName='0F')
                        body_temperature = patientVitals(encounterId=encounter_details, vitalTypeCode=vitalTypeCode,
                                                         vitalStatus=vitalStatus,
                                                         vitalSignResultValue=str(values['body_temperature']),
                                                         vitalSignResultUnit=vitalSignResultUnit)
                        body_temperature.save()
                if 'heart_rate' in request.POST:
                    if values['heart_rate'] != '':
                        vitalTypeCode = vitalSignsResultType.objects.get(vitalSignsResultTypeName='Heart Rate')
                        vitalStatus = vitalSignsResultStatus.objects.get(vitalSignsResultStatusCode='2')
                        vitalSignResultUnit = unitOfMeasurement.objects.get(unitOfMeasurementShortName='/min')
                        heart_rate = patientVitals(encounterId=encounter_details, vitalTypeCode=vitalTypeCode,
                                                   vitalStatus=vitalStatus, vitalSignResultValue=str(values['heart_rate']),
                                                   vitalSignResultUnit=vitalSignResultUnit)
                        heart_rate.save()
                if 'oxygen_saturation' in request.POST:
                    if values['oxygen_saturation'] != '':
                        vitalTypeCode = vitalSignsResultType.objects.get(vitalSignsResultTypeName='Oxygen Saturation')
                        vitalStatus = vitalSignsResultStatus.objects.get(vitalSignsResultStatusCode='2')
                        vitalSignResultUnit = unitOfMeasurement.objects.get(unitOfMeasurementShortName='%')
                        oxygen_saturation = patientVitals(encounterId=encounter_details, vitalTypeCode=vitalTypeCode,
                                                          vitalStatus=vitalStatus,
                                                          vitalSignResultValue=str(values['oxygen_saturation']),
                                                          vitalSignResultUnit=vitalSignResultUnit)
                        oxygen_saturation.save()
                if values['complaint'] != '':
                    complaints = request.POST.getlist('complaint')
                    body_site = request.POST.getlist('body_site')
                    duration = request.POST.getlist('duration')
                    duration_unit = request.POST.getlist('duration_unit')
                    for counter, complaint in enumerate(complaints):
                        complaint_id = complaint.split(' ')[0] + str((datetime.now(timezone.utc) + timedelta(
                            seconds=(5 * 3600) + 1800)).timestamp()).split('.')[0]
                        site = body_site[counter]
                        complaint_site = bodySite.objects.get(bodySiteName=site)
                        patient_complaints = patientComplaints(encounterId=encounter_details, chiefComplaintId=complaint_id,
                                                               chiefComplaintName=complaint,
                                                               chiefComplaintBodySite=complaint_site,
                                                               chiefComplaintDuration=duration[counter],
                                                               chiefComplaintDurationUnit=duration_unit[counter])
                        patient_complaints.save()
                        prescription_deletion = file_created_details(file_id=prescription_id,
                                                                     details_id=patient_complaints.id,
                                                                     details_type='complaint')
                        prescription_deletion.save()
                if 'health_condition' in request.POST:
                    if values['health_condition'] != '':
                        relationship = request.POST.getlist('relationship')
                        health_condition = request.POST.getlist('health_condition')
                        member_condition_status = request.POST.getlist('member_condition_status')
                        for counter, relation in enumerate(relationship):
                            familyMemberUidNumber = relation + str(patient_details.id)
                            pr = familyMemberRelationship.objects.get(familyMemberRelationshipName=relation)
                            health_cs = healthConditionStatus.objects.get(
                                healthConditionStatusDescription=member_condition_status[counter])
                            member_condition_code = healthCondition.objects.get(
                                healthConditionName=health_condition[counter]).healthConditionCode
                            try:
                                family_history = familyHistory.objects.get(familyIdentifier=encounter_details,
                                                                           familyMemberRelationship=relationship,
                                                                           healthConditionCode=member_condition_code)
                                family_history.familyMemberHealthConditionStatus = health_cs
                                family_history.save()
                            except familyHistory.DoesNotExist:
                                family_history = familyHistory(familyIdentifier=encounter_details,
                                                               familyMemberUidNumber=familyMemberUidNumber,
                                                               familyMemberRelationship=pr,
                                                               familyMemeberHealthCondition=health_condition[counter],
                                                               healthConditionCode=member_condition_code,
                                                               familyMemberHealthConditionStatus=health_cs)
                                family_history.save()
                                prescription_deletion = file_created_details(file_id=prescription_id,
                                                                             details_id=family_history.id,
                                                                             details_type='family')
                                prescription_deletion.save()
                if 'existing_comorbidities' in request.POST:
                    if values['existing_comorbidities'] != '':
                        existing_comorbidities = request.POST.getlist('existing_comorbidities')
                        health_condition_status = request.POST.getlist('health_condition_status')
                        for counter, comorbidity in enumerate(existing_comorbidities):
                            health_status_patient = healthConditionStatus.objects.get(
                                healthConditionStatusDescription=health_condition_status[counter])
                            member_condition_code = healthCondition.objects.get(
                                healthConditionName=existing_comorbidities[counter]).healthConditionCode
                            try:
                                patient_comorbidities = patientComorbidities.objects.get(patientId=encounter_details,
                                                                                         comorbidityHealthConditionCode=member_condition_code)
                                patient_comorbidities.comorbidityHealthConditionStatus = health_status_patient
                                patient_comorbidities.save()
                            except patientComorbidities.DoesNotExist:
                                patient_comorbidities = patientComorbidities(patientId=encounter_details,
                                                                             comorbidityHealthCondition=comorbidity,
                                                                             comorbidityHealthConditionCode=member_condition_code,
                                                                             comorbidityHealthConditionStatus=health_status_patient)
                                patient_comorbidities.save()
                                prescription_deletion = file_created_details(file_id=encounter_details,
                                                                             details_id=patient_comorbidities.id,
                                                                             details_type='comorbidities')
                                prescription_deletion.save()
                if 'allergy_from' in request.POST:
                    allergy_from = request.POST.getlist('allergy_from')
                    allergy_severity = request.POST.getlist('allergy_severity')
                    allergy_status = request.POST.getlist('allergy_status')
                    for counter, allergies in enumerate(allergy_from):
                        allergy_code = allergyProduct.objects.get(allergyProductDescription=allergies)
                        allergy_status_code = healthConditionStatus.objects.get(
                            healthConditionStatusDescription=allergy_status[counter])
                        allergy_severity_code = severityCodes.objects.get(severityDescription=allergy_severity[counter])
                        try:
                            patient_allergies = patientAllergies.objects.get(patientId=encounter_details,
                                                                             allergyCode=allergy_code)
                            patient_allergies.allergyStatusCode = allergy_status_code
                            patient_allergies.allergySeverityCode = allergy_severity_code
                            patient_allergies.save()
                        except:
                            patient_allergies = patientAllergies(patientId=encounter_details, allergyCode=allergy_code,
                                                                 allergyStatusCode=allergy_status_code,
                                                                 allergySeverityCode=allergy_severity_code)
                            patient_allergies.save()
                            prescription_deletion = file_created_details(file_id=prescription_id,
                                                                         details_id=patient_allergies.id,
                                                                         details_type='allergies')
                            prescription_deletion.save()
                if values['examination_notes'] != '':
                    examination_type = examinationType.objects.get(examinationTypeCode='01')
                    examination_findings = values['examination_notes']
                    system_examined = organSystem.objects.get(organSystemName=values['examined_system'])
                    encounter_examination = encounter_examination_details(encounter_id=encounter_details,
                                                                          examination_type=examination_type,
                                                                          system_examined=system_examined,
                                                                          examination_notes=examination_findings,
                                                                          examination_date=saving_date)
                    encounter_examination.save()
                    prescription_deletion = file_created_details(file_id=prescription_id,
                                                                 details_id=encounter_examination.id,
                                                                 details_type='examination')
                    prescription_deletion.save()
                if values['diagnosis_name'] != '':
                    condition_name = request.POST.getlist('diagnosis_name')
                    diagnosis_type = request.POST.getlist('diagnosis_type')
                    for counter, conditions in enumerate(condition_name):
                        condition_code = healthCondition.objects.get(healthConditionName=conditions)
                        condition_type = condition_code.health_condition_type.healthConditionTypeName
                        condition_status = healthConditionStatus.objects.get(healthConditionStatusCode='01')
                        encounter_diagnosis = encounter_diagnosis_details(encounter_id=encounter_details,
                                                                          condition_code=condition_code.healthConditionCode,
                                                                          condition_type=condition_type,
                                                                          condition_status=condition_status,
                                                                          diagnosis_type=diagnosis_type[counter],
                                                                          diagnosed_condition_name=conditions,
                                                                          diagnosis_date=saving_date)
                        encounter_diagnosis.save()
                        prescription_deletion = file_created_details(file_id=prescription_id,
                                                                     details_id=encounter_diagnosis.id,
                                                                     details_type='diagnosis')
                        prescription_deletion.save()

                    # order_status =
                if values['test_name'] != '':
                    diagnostic_test = request.POST.getlist('test_name')
                    for tests in diagnostic_test:
                        try:
                            lab_test_code = labOrderCode.objects.get(loincDisplayName=tests).loincCode
                        except labOrderCode.DoesNotExist:
                            lab_test_code = None
                        test_status = vitalSignsResultStatus.objects.get(vitalSignsResultStatusCode='5')
                        lab_test_details = encounter_lab_tests(encounter_id=encounter_details, lab_test_status=test_status,
                                                               lab_test_code=lab_test_code, lab_test_name=tests,
                                                               lab_test_date=saving_date)
                        lab_test_details.save()
                        prescription_deletion = file_created_details(file_id=prescription_id,
                                                                     details_id=lab_test_details.id, details_type='tests')
                        prescription_deletion.save()
                if values['med_name'] != '':
                    medicine_name = request.POST.getlist('med_name')
                    morning_dose = request.POST.getlist('morning')
                    afternoon_dose = request.POST.getlist('afternoon')
                    evening_dose = request.POST.getlist('evening')
                    night_dose = request.POST.getlist('night')
                    dosage_unit = request.POST.getlist('dosage_unit')
                    frequency_unit = request.POST.getlist('frequency_unit')
                    duration = request.POST.getlist('duration')
                    duration_unit = request.POST.getlist('duration_unit')
                    consume_time = request.POST.getlist('consume_time')
                    prescription_notes = request.POST.getlist('prescription_notes')
                    for counter, meds in enumerate(medicine_name):
                        try:
                            name_check = medicine_generic_data.objects.get(full_medicine_name=meds)
                            generic_name = name_check.generic_name
                            # medicine_form = name_check.medicine_type
                            medicine_form = None
                        except master_list_of_medicines.DoesNotExist:
                            generic_name = None
                            medicine_form = None
                        prescribed_medicines = encounter_prescribed_medicines(encounter_id=encounter_details,
                                                                              order_id=encounter_details.encounterId,
                                                                              medicine_name=meds, generic_name=generic_name,
                                                                              morning_dose=morning_dose[counter],
                                                                              afternoon_dose=afternoon_dose[counter],
                                                                              evening_dose=evening_dose[counter],
                                                                              night_dose=night_dose[counter],
                                                                              medicine_dose_unit=dosage_unit[counter],
                                                                              medicine_frequency_unit=frequency_unit[
                                                                                  counter], medicine_form=medicine_form,
                                                                              medicine_duration=duration[counter],
                                                                              medicine_duration_unit=duration_unit[counter],
                                                                              consume_time=consume_time[counter],
                                                                              consumption_note=prescription_notes[counter],
                                                                              medicine_date=saving_date)
                        prescribed_medicines.save()
                        prescription_deletion = file_created_details(file_id=prescription_id,
                                                                     details_id=prescribed_medicines.id,
                                                                     details_type='medicines')
                        prescription_deletion.save()
                if values['instructions'] != '':
                    followup_instructions = values['instructions']
                else:
                    followup_instructions = None
                if values['followup_date'] != '':
                    followup_date = values['followup_date']
                else:
                    followup_date = None
                followup_details = encounter_followup_details(encounter_id=encounter_details,
                                                              followup_instructions=followup_instructions,
                                                              followup_date=followup_date,
                                                              followup_created_date=saving_date)
                followup_details.save()
                prescription_deletion = file_created_details(file_id=prescription_id, details_id=followup_details.id,
                                                             details_type='followup')
                prescription_deletion.save()
                # prescription parameters

                encounter_notes_document['patient_id'] = patient_details.ProvidersPatientID
                encounter_notes_document['prescription_id'] = prescription_id.id
                encounter_notes_document[
                    'facility_id'] = encounter_details.uniqueFacilityIdentificationNumber.facilityRegistrationNumber
                encounter_notes_document['encounter_id'] = encounter_details.encounterId
                encounter_notes_document['encounter_date_time'] = encounter_details.encounterDate
                encounter_notes_document[
                    'provider_registration_number'] = provider_details.uniqueIndividualHealthCareProviderNumber
                encounter_notes_document['provider_name'] = provider_details.providerName
                encounter_notes_document['provider_qualifications'] = provider_qualifications.objects.filter(
                    providerDetailsCode=provider_details)
                encounter_notes_document['patient_name'] = patient_details.PatientName
                encounter_notes_document['patient_dob'] = patient_details.PatientDOB
                encounter_notes_document['patient_gender'] = patient_details.PatientGender
                encounter_notes_document['patient_address'] = patient_details.PatientAddress
                encounter_notes_document['patient_class'] = 'Outpatient'
                encounter_notes_document['patient_allergies'] = patientAllergies.objects.filter(patientId=encounter_details)
                encounter_notes_document['patient_comorbidities'] = patientComorbidities.objects.filter(
                    patientId=encounter_details)
                encounter_notes_document['patient_complaints'] = patientComplaints.objects.filter(
                    encounterId=encounter_details)
                encounter_notes_document['encounter_examination_details'] = encounter_examination_details.objects.filter(
                    encounter_id=encounter_details, examination_date=saving_date)
                encounter_notes_document['encounter_diagnosis_details'] = encounter_diagnosis_details.objects.filter(
                    encounter_id=encounter_details, diagnosis_date=saving_date)
                encounter_notes_document['encounter_lab_tests'] = encounter_lab_tests.objects.filter(
                    encounter_id=encounter_details, lab_test_date=saving_date)
                encounter_notes_document['encounter_prescribed_medicines'] = encounter_prescribed_medicines.objects.filter(
                    encounter_id=encounter_details, medicine_date=saving_date)
                encounter_notes_document['encounter_followup_details'] = encounter_followup_details.objects.filter(
                    encounter_id=encounter_details, followup_created_date=saving_date)
                static_url = os.path.dirname(__file__) + "\static\\doctor_consultation\images\\transparent_logo.png"
                template = get_template("doctor_consultation\\encounter_generate_prescription.html")
                context = {'template_name': template_name, 'details': encounter_notes_document, 'static_url': static_url}
                prescription_final = template.render(context)
                config = imgkit.config(wkhtmltoimage=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe')
                file_name_pres = encounter_details.encounterId + '_' + str(time.mktime(datetime.now().timetuple()))[
                                                                       :-2] + '_all.jpeg'
                pres_image = imgkit.from_string(prescription_final, False, config=config)
                fh = tempfile.NamedTemporaryFile(delete=False)
                fh.write(pres_image)
                prescription_id.file_saved.save(file_name_pres, File(fh))
                prescription_id.order_id = encounter_details.encounterId
                prescription_id.file_name = file_name_pres
                prescription_id.file_type = 'jpg'
                prescription_id.save()
                # mnop
                # signed_file = os.path.join("C:\\", file_name_pres + '.sig')
                # gpg = gnupg.GPG(gnupghome="C:\\Users\\Administrator\\AppData\\Roaming\\gnupg")
                # f = prescription_id.file_saved.open('r')
                # status = gpg.sign_file(f, keyid='14643844CD17241019B0E2DA50B5F5A30A51DEBB', passphrase='testsigning', clearsign=True, output=signed_file)
                # logging.debug(status.status)
                # logging.debug(status.stderr)
                # r = request_dump(dump = status.status, source = 'gpg')
                # r.save()
                # r = request_dump(dump = status.stderr, source = 'gpg')
                # r.save()
                # f.close
                fh.close()
                os.remove(fh.name)
                new_case_dict = assign_same_encounter(encounter_details.encounterId, provider_details)
                return render(request, 'doctor_consultation/facility_consultation.html',
                              {'template_name': template_name, 'vc': vc, 'encounter_details': new_case_dict})
            elif 'delete' in request.POST:
                file_id = values['file_id']
                order_id = values['order_id']
                try:
                    del_file = files_created_during_encounter.objects.get(id=file_id)
                    detials_to_delete = file_created_details.objects.filter(file_id=del_file)
                    for details in detials_to_delete:
                        if details.details_type == 'complaint':
                            del_complaint = patientComplaints.objects.get(id=details.details_id)
                            del_complaint.delete()
                        elif details.details_type == 'family':
                            del_family = familyHistory.objects.get(id=details.details_id)
                            del_family.delete()
                        elif details.details_type == 'comorbidities':
                            del_comorbidities = patientComorbidities.objects.get(id=details.details_id)
                            del_comorbidities.delete()
                        elif details.details_type == 'allergies':
                            del_allergies = patientAllergies.objects.get(id=details.details_id)
                            del_allergies.delete()
                        elif details.details_type == 'examination':
                            del_examination = encounter_examination_details.objects.get(id=details.details_id)
                            del_examination.delete()
                        elif details.details_type == 'diagnosis':
                            del_diagnosis = encounter_diagnosis_details.objects.get(id=details.details_id)
                            del_diagnosis.delete()
                        elif details.details_type == 'tests':
                            del_tests = encounter_lab_tests.objects.get(id=details.details_id)
                            del_tests.delete()
                        elif details.details_type == 'medicines':
                            del_medicines = encounter_prescribed_medicines.objects.get(id=details.details_id)
                            del_medicines.delete()
                        elif details.details_type == 'followup':
                            del_followup = encounter_followup_details.objects.get(id=details.details_id)
                            del_followup.delete()
                    del_file.delete()
                    new_case_dict = assign_same_encounter(order_id, provider_details)
                    return render(request, 'doctor_consultation/facility_consultation.html',
                                  {'template_name': template_name, 'vc': vc, 'encounter_details': new_case_dict})
                except new_prescription_files.DoesNotExist:
                    new_case_dict = assign_same_encounter(encounter_details.encounterId, provider_details)
                    return render(request, 'doctor_consultation/facility_consultation.html',
                                  {'template_name': template_name, 'vc': vc, 'encounter_details': new_case_dict})
            elif 'upload_details' in request.POST:
                order_id = values['request_id']
                status_update = encounter_status.objects.get(order_id=order_id)
                status_update.order_status = 2
                status_update.last_status_update_date = datetime.now(timezone.utc) + timedelta(seconds=(5 * 3600) + 1800)
                episode_status = episodeStatus.objects.get(episodeStatusCode='2')
                status_update.episodeStatusId = episode_status
                status_update.save()
                encounter_details = encounterDetails.objects.get(encounterId=order_id)
                order_status = orderStatus.objects.get(orderStatusCode='SC')
                order_update = order_details.objects.get(encounter_id=encounter_details, order_type='OPD',
                                                         order_status=order_status)
                new_order_status = orderStatus.objects.get(orderStatusCode='CM')
                order_update.order_status = new_order_status
                order_update.save()
                # sms update
                init_msg = "Based on your consultation, " + status_update.case_assigned_to.providerName + " from LetsDoc has shared the care plan. Please click here "
                encounter_files = files_created_during_encounter.objects.filter(encounter_id=encounter_details)
                url_add = ''
                for files in encounter_files:
                    url_add = url_add + files.file_saved.url + ', '
                msg_encode = init_msg + url_add + "to view the care plan." + "\nFor feedback or any concern regarding LetsDoc services please email to " + "support@letsdoc.in"
                sms_msg = msg_encode
                payload = {}
                payload['userId'] = sms_user_id_trans
                payload['appid'] = "lhtalt"
                payload['pass'] = sms_pswd_trans
                payload['contenttype'] = "1"
                payload['from'] = "LTSDOC"
                patient_details_for_upload = Patient.objects.get(ProvidersPatientID=encounter_details.patientId)
                payload['to'] = "91" + patient_details_for_upload.patientMobileNumber
                payload['selfid'] = "true"
                payload['intflag'] = "false"
                payload['text'] = sms_msg
                payload['s'] = "1"
                payload['alert'] = "1"
                payload['dpi'] = "1201159523893139905"
                payload['dtm'] = "1007163428329299948"
                payload['tc'] = "3"
                data = json.dumps(payload)
                b = request_dump(dump=data, source='sms_request')
                b.save()
                headers = {}
                headers['Content-type'] = "application/json"
                # r = requests.post(url_sms, data = json.dumps(payload),headers={'Content-type': 'application/json'})
                r = requests.request("POST", url_sms, data=data, headers=headers)
                k = r.content
                a = (r.text + str(k) + str(r.status_code))
                b = request_dump(dump=a, source='sms_response')
                b.save()
                # WhatsApp
                # message_payload = {}
                # message_payload['messages'] = []
                # message_details = {}
                # message_details['sender'] = sender
                # message_details['to'] = "91" + encounter_details.patientId.patientcontactdetails_set.all().order_by('-id')[0].patientMobile
                # message_details['channel'] = "wa"
                # message_details['type'] = 'mediaTemplate'
                # message_details['mediaTemplate'] = {}
                # message_details['mediaTemplate']['mediaUrl'] = url_add
                # message_details['mediaTemplate']['contentType'] = 'image/jpeg'
                # message_details['mediaTemplate']['template'] = '1007163428329299948'
                # message_details['mediaTemplate']['parameters'] = {}
                # message_details['mediaTemplate']['parameters']['1'] = status_update.case_assigned_to.providerName
                # message_details['mediaTemplate']['parameters']['2'] = 'support@letsdoc.in'
                # message_details['mediaTemplate']['langCode'] = "en"
                # message_payload['messages'].append(message_details)
                # message_payload['responseType'] = 'json'
                # message_url = whatsapp_message_url
                # headers = {}
                # headers['Content-type'] = "application/json"
                # headers['user'] = test_entreprise_id
                # headers['pass'] = "letsduat19"
                # headers['Sender'] = "916364378884"
                # r = requests.request("POST", message_url, data = json.dumps(message_payload), headers = headers)
                # k = r.content
                # a = json.dumps(message_payload) + (r.text + str(k) + str(r.status_code))
                # b = request_dump(dump = a, source = 'whatsapp_doctor_update')
                # b.save()
                # WhatsApp
                message_payload = {}
                message_payload['messages'] = []
                message_details = {}
                message_details['sender'] = sender
                patient_details_for_upload = Patient.objects.get(ProvidersPatientID=encounter_details.patientId)
                message_details['to'] = "91" + patient_details_for_upload.patientMobileNumber
                message_details['channel'] = "wa"
                message_details['type'] = 'template'
                message_details['template'] = {}
                message_details['template']['body'] = []
                template_body = {}
                template_body["type"] = "text"
                template_body['text'] = status_update.case_assigned_to.providerName
                message_details['template']['body'].append(template_body)
                template_body = {}
                template_body["type"] = "text"
                template_body['text'] = url_add
                message_details['template']['body'].append(template_body)
                template_body = {}
                template_body["type"] = "text"
                template_body['text'] = "support@letsdoc.in"
                message_details['template']['body'].append(template_body)
                message_details['template']['templateId'] = '1007163280523479319'
                message_details['template']['langCode'] = "en"
                message_payload['messages'].append(message_details)
                message_payload['responseType'] = 'json'
                message_url = whatsapp_message_url
                headers = {}
                headers['Content-type'] = "application/json"
                headers['user'] = test_entreprise_id
                headers['pass'] = sender_pass
                headers['Sender'] = sender
                r = requests.request("POST", message_url, data=json.dumps(message_payload), headers=headers)
                k = r.content
                a = json.dumps(message_payload) + (r.text + str(k) + str(r.status_code))
                b = request_dump(dump=a, source='whatsapp_doctor_update')
                b.save()
                if encounter_details.uniqueFacilityIdentificationNumber.abdm_flows:
                    person_details = patient_details_for_upload.person_patientId
                    abha_check = personAbhaIds.objects.filter(person_patientId=person_details)
                    if abha_check.count() == 0:
                        abha_notify_sms(patient_details_for_upload.patientMobileNumber, person_details.facility_personID)
                    else:
                        check_linked_contect = careContexts.objects.filter(encounter_id=encounter_details,
                                                                           linked_request_for=True,
                                                                           linked_status=True)
                        if check_linked_contect.count() == 0:
                            abha_care_context_linking(patient_details_for_upload, encounter_details)
                        else:
                            care_context_link = str(check_linked_contect.order_by('-id')[0].care_context_uid)
                            abha_linking_notification(abha_check, encounter_details, care_context_link)
                encounter_retry_update()  # updates encounter status and episode status based on followup date
                provider_login_check()
                new_case_dict = assign_encounter(provider_email)
                return render(request, 'doctor_consultation/facility_consultation.html',
                              {'template_name': template_name, 'vc': vc, 'encounter_details': new_case_dict})
            else:
                encounter_details = get_encounter_details(eId, prId, access_token)
                print("ajdfdkjfdfj")
                print(encounter_details)
                return render(request, 'consultation/opd_consultation.html', {'encounter_details':encounter_details})
        else:
            return redirect(doctor_profile)