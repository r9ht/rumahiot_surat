from django.shortcuts import render,HttpResponse
from rumahiot_surat.apps.notification.utils import ResponseGenerator, RequestUtils
import json
from rumahiot_surat.apps.notification.forms import EmailActivationForm, EmailWelcomeForm, DeviceNotificationEmail
from rumahiot_surat.settings import SECRET_KEY, SURAT_MAILGUN_DOMAIN_NAME, SURAT_MAILGUN_API_KEY
from rumahiot_surat.apps.notification.mailgun import MailGun
from django.views.decorators.csrf import csrf_exempt
from rumahiot_surat.settings import SIDIK_EMAIL_ACTIVATION_ENDPOINT
from datetime import datetime

# Create your views here.
# todo : log every email sent ?

@csrf_exempt
def email_activation(request):

    # Class import
    rg = ResponseGenerator()
    requtils = RequestUtils()
    mg = MailGun()

    if request.method == 'POST' :
        try:
            token = requtils.get_access_token(request)
        except KeyError:
            response_data = rg.error_response_generator(400, 'Please define the authorization header')
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
        else:
            if token['token'] is None:
                response_data = rg.error_response_generator(400, token['error'])
                return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
            else:
                form = EmailActivationForm(request.POST)
                if form.is_valid():
                    # TODO : Fix this soon
                    if token['token'] == SECRET_KEY:
                        result = mg.send_simple_message(
                            domain_name=SURAT_MAILGUN_DOMAIN_NAME,
                            api_key=SURAT_MAILGUN_API_KEY,
                            sender='security',
                            sender_name='Rumah IoT',
                            recipient_list=[form.cleaned_data['email']],
                            subject='Please verify your Rumah IoT account',
                            text='Hi,\n\nThanks for registering in Rumah IoT ! Please '
                                    'confirm your email address by clicking the link supplied '
                                    'below\n\n{}/{}\n\n'
                                    'If you did not sign up for a Rumah IoT account please omit this email\n\n'
                                    'Regards\nRumah IoT Team'.format(SIDIK_EMAIL_ACTIVATION_ENDPOINT,form.cleaned_data['activation_uuid'])
                        )

                        if result.status_code == 200:
                            data = {
                                'message' : 'Activation email sent',
                                'activation_uuid': form.cleaned_data['activation_uuid'],
                                'email': form.cleaned_data['email']
                            }
                            response_data = rg.data_response_generator(data)
                            return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)

                        else:
                            response_data = rg.error_response_generator(500, 'Internal server error')
                            return HttpResponse(json.dumps(response_data), content_type='application/json', status=500)


                    else:
                        response_data = rg.error_response_generator(400, 'Invalid authorization key')
                        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
                else:
                    response_data = rg.error_response_generator(400, 'Invalid or missing parameter submitted')
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)



@csrf_exempt
def welcome_email(request):

    # Class import
    rg = ResponseGenerator()
    requtils = RequestUtils()
    mg = MailGun()

    if request.method == 'POST' :
        try:
            token = requtils.get_access_token(request)
        except KeyError:
            response_data = rg.error_response_generator(400, 'Please define the authorization header')
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
        else:
            if token['token'] is None:
                response_data = rg.error_response_generator(400, token['error'])
                return HttpResponse(json.dumps(response_data), content_type='application/json', status=403)
            else:
                form = EmailWelcomeForm(request.POST)
                if form.is_valid():
                    # TODO : Fix this secret key, create an automated for key changing
                    if token['token'] == SECRET_KEY:
                        result = mg.send_simple_message(
                            domain_name=SURAT_MAILGUN_DOMAIN_NAME,
                            api_key=SURAT_MAILGUN_API_KEY,
                            sender='no-reply',
                            sender_name='Rumah IoT',
                            recipient_list=[form.cleaned_data['email']],
                            subject='Welcome to Rumah IoT',
                            text='Hi,\n\nThanks for confirming your email address, have fun building your amazing things :D\n\n'
                                    'Regards\nRumah IoT Team'
                        )
                        if result.status_code == 200:
                            data = {
                                'message' : 'Welcome email sent',
                                'email': form.cleaned_data['email']
                            }
                            response_data = rg.data_response_generator(data)
                            return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)

                        else:
                            response_data = rg.error_response_generator(500, 'Internal server error')
                            return HttpResponse(json.dumps(response_data), content_type='application/json', status=500)


                    else:
                        response_data = rg.error_response_generator(400, 'Invalid authorization key')
                        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
                else:
                    response_data = rg.error_response_generator(400, 'Invalid or missing parameter submitted')
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

# NOTE : THERE WILL BE NOTIFICATION THAT SENT TO OTHER ENDPOINT FOR MOBILE CLIENT
# THE MOBILE NOTIFICATION WILL BE REMOVED AFTER ALPHA RELEASE
@csrf_exempt
def device_notification_email(request):
    # Class import
    rg = ResponseGenerator()
    requtils = RequestUtils()
    mg = MailGun()

    if request.method == 'POST':
        try:
            token = requtils.get_access_token(request)
        except KeyError:
            response_data = rg.error_response_generator(400, 'Please define the authorization header')
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
        else:
            if token['token'] is None:
                response_data = rg.error_response_generator(400, token['error'])
                return HttpResponse(json.dumps(response_data), content_type='application/json', status=403)
            else:
                form = DeviceNotificationEmail(request.POST)
                if form.is_valid():
                    # TODO : Fix this secret key, create an automated for key changing
                    if token['token'] == SECRET_KEY:
                        # Normalize the direction
                        threshold_direction = ''
                        if form.cleaned_data['threshold_direction'] == '1':
                            threshold_direction = 'Above'
                        elif form.cleaned_data['threshold_direction'] == '-1':
                            threshold_direction = 'Below'

                        if form.cleaned_data['notification_type'] == '0' :
                            email_body = 'Hi there , we are notifying that current value of sensor {} on device {} is {}{} at {}, {} ' \
                                         'the set threshold value which is {}{}, There will be no more notification unless the latest ' \
                                         'value is going back to normal and we will let you know when it happens' \
                                         '\n\nRegards\nRumah IoT Team'.format(form.cleaned_data['user_sensor_name'],
                                                                              form.cleaned_data['device_name'],
                                                                              form.cleaned_data['latest_value'],
                                                                              form.cleaned_data['unit_symbol'],
                                                                              datetime.fromtimestamp(
                                                                                  float(form.cleaned_data['time_reached'])).strftime(
                                                                                  '%d-%m-%Y %H:%M:%S'),
                                                                              threshold_direction,
                                                                              form.cleaned_data['threshold_value'],
                                                                              form.cleaned_data['unit_symbol'])

                        elif form.cleaned_data['notification_type'] == '1' :
                            email_body = 'Hi, this is a proceeding information from the last notification, we are notifying ' \
                                         'you that the current value of sensor {} on device {} is going back to normal , {}{} at {}' \
                                         '\n\nRegards\nRumah IoT Team'.format(form.cleaned_data['user_sensor_name'],
                                                                              form.cleaned_data['device_name'],
                                                                              form.cleaned_data['latest_value'],
                                                                              form.cleaned_data['unit_symbol'],
                                                                              datetime.fromtimestamp(float(form.cleaned_data['time_reached'])).strftime(
                                                                                  '%d-%m-%Y %H:%M:%S'))
                        else:
                            # Todo : Make sure about the email type in the form model
                            email_body = 'Regards\nRumah IoT Team'

                        result = mg.send_simple_message(
                            domain_name=SURAT_MAILGUN_DOMAIN_NAME,
                            api_key=SURAT_MAILGUN_API_KEY,
                            sender='notification',
                            sender_name='Rumah IoT Notification',
                            recipient_list=[form.cleaned_data['email']],
                            subject='Notification for Device : {}'.format(form.cleaned_data['device_name']),
                            text=email_body
                        )
                        if result.status_code == 200:
                            data = {
                                'message': 'Device notification email sent',
                                'email': form.cleaned_data['email']
                            }
                            response_data = rg.data_response_generator(data)
                            return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)

                        else:
                            response_data = rg.error_response_generator(500, 'Internal server error')
                            return HttpResponse(json.dumps(response_data), content_type='application/json', status=500)

                else:
                    response_data = rg.error_response_generator(400, 'Invalid or missing parameter submitted')
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
