from django.shortcuts import render, HttpResponse
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rumahiot_surat.apps.notification.utils import ResponseGenerator, RequestUtils
from rumahiot_surat.apps.logger.forms import DeviceSensorNotificationForm
from rumahiot_surat.settings import SECRET_KEY
from rumahiot_surat.apps.logger.mongodb import SuratMongoDB
from rumahiot_surat.apps.sidik_module.authorization import SuratSidikModule
from uuid import uuid4
import pymongo

# Create your views here.

# For panel device notification in the top right corner
@csrf_exempt
def device_panel_notification(request):
    # Class import
    rg = ResponseGenerator()
    requtils = RequestUtils()
    db = SuratMongoDB()

    if request.method == 'POST':
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
                form = DeviceSensorNotificationForm(request.POST)
                if form.is_valid():
                    if token['token'] == SECRET_KEY:
                        try :
                            # generate json structure for log
                            data = {
                                'device_sensor_notification_log_uuid': uuid4().hex,
                                'user_uuid': form.cleaned_data['user_uuid'],
                                'device_uuid': form.cleaned_data['device_uuid'],
                                'device_name': form.cleaned_data['device_name'],
                                'user_sensor_uuid': form.cleaned_data['user_sensor_uuid'],
                                'user_sensor_name': form.cleaned_data['user_sensor_name'],
                                'threshold_value': float(form.cleaned_data['threshold_value']),
                                'latest_value': float(form.cleaned_data['latest_value']),
                                'time_reached': float(form.cleaned_data['time_reached']),
                                'threshold_direction': form.cleaned_data['threshold_direction'],
                                'unit_symbol': form.cleaned_data['unit_symbol'],
                                'notification_type': form.cleaned_data['notification_type'],
                                'sent': form.cleaned_data['sent'],
                                'viewed': form.cleaned_data['viewed']
                            }

                        # When one of the value is not in a correct format (failed to typecasted)
                        except :
                            response_data = rg.error_response_generator(400, 'Invalid value submitted')
                            return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
                        else:
                            try:
                                result = db.put_device_notification_log(data=data)
                            # For unknown error
                            except:
                                response_data = rg.error_response_generator(500, 'Internal server error')
                                return HttpResponse(json.dumps(response_data), content_type='application/json',
                                                    status=500)
                            else:
                                response_data = rg.success_response_generator(200, 'Log data successfully submitted')
                                return HttpResponse(json.dumps(response_data), content_type='application/json',
                                                    status=200)
                    else:
                        response_data = rg.error_response_generator(400, 'Invalid authorization key')
                        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
                else:
                    response_data = rg.error_response_generator(400, 'Invalid or missing parameter submitted')
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)


# For changing viewed status on a specific device notification
def clear_device_panel_notification(request, device_sensor_notification_log_uuid):
    # Class import
    rg = ResponseGenerator()
    requtils = RequestUtils()
    db = SuratMongoDB()
    auth = SuratSidikModule()

    if request.method == 'GET' :
        try:
            token = requtils.get_access_token(request)
        except KeyError:
            response_data = rg.error_response_generator(400, 'Please define the authorization header')
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
        else:
            if token['token'] != None:
                user = auth.get_user_data(token['token'])
                if user['user_uuid'] != None:
                    # get the notification log
                    log = db.get_notification_log_by_uuid(device_sensor_notification_log_uuid=device_sensor_notification_log_uuid, viewed='0')
                    if log != None:
                        # check the owenership
                        if user['user_uuid'] == log['user_uuid']:
                            try :
                                # Update the viewed status
                                db.update_notification_log_viewed_status(object_id=log['_id'], new_viewed_status='1')
                            except:
                                # For unknown error
                                response_data = rg.error_response_generator(500, 'Internal server error')
                                return HttpResponse(json.dumps(response_data), content_type='application/json',
                                                    status=500)
                            else:
                                response_data = rg.success_response_generator(200, 'Device notification log status successfully changed')
                                return HttpResponse(json.dumps(response_data), content_type='application/json',
                                                    status=200)
                        else:
                            response_data = rg.error_response_generator(400, 'Invalid device notification log uuid')
                            return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
                    else:
                        response_data = rg.error_response_generator(400, 'Invalid device notification log uuid')
                        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

                else:
                    response_data = rg.error_response_generator(400, user['error'])
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

# For changing viewed status for all device notification
def clear_all_device_panel_notification(request):
    # Class import
    rg = ResponseGenerator()
    requtils = RequestUtils()
    db = SuratMongoDB()
    auth = SuratSidikModule()

    if request.method == 'GET' :
        try:
            token = requtils.get_access_token(request)
        except KeyError:
            response_data = rg.error_response_generator(400, 'Please define the authorization header')
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
        else:
            if token['token'] != None:
                user = auth.get_user_data(token['token'])
                if user['user_uuid'] != None:
                    # get the notification log
                    logs = db.get_notification_log_by_user_uuid(user_uuid=user['user_uuid'], viewed='0', direction=pymongo.DESCENDING)
                    if logs.count() != 0:
                        # clear all the log
                        for log in logs:
                            db.update_notification_log_viewed_status(object_id=log['_id'], new_viewed_status='1')
                        response_data = rg.success_response_generator(200, 'All device notification log status successfully cleared')
                        return HttpResponse(json.dumps(response_data), content_type='application/json',
                                                    status=200)
                    else:
                        response_data = rg.success_response_generator(200, 'All device notification log successfully cleared')
                        return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)

                else:
                    response_data = rg.error_response_generator(400, user['error'])
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)


# For getting all device panel notification
def get_all_device_panel_notification(request):
    # Class import
    rg = ResponseGenerator()
    requtils = RequestUtils()
    db = SuratMongoDB()
    auth = SuratSidikModule()

    if request.method == 'GET' :
        try:
            token = requtils.get_access_token(request)
        except KeyError:
            response_data = rg.error_response_generator(400, 'Please define the authorization header')
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
        else:
            if token['token'] != None:
                user = auth.get_user_data(token['token'])
                if user['user_uuid'] != None:
                    # get the notification log
                    # Defaulting
                    logs = db.get_notification_log_by_user_uuid(user_uuid=user['user_uuid'], viewed='0', direction=pymongo.DESCENDING)
                    # Data for notification response
                    data = {
                        'device_notification_logs_count' : int(logs.count()),
                        'device_notification_logs': [],
                        'time_grabbed': float(datetime.now().timestamp())
                    }

                    for log in logs :
                        # Device notification log data for device_notification_logs list
                        device_notification_log = {}
                        device_notification_log['device_sensor_notification_log_uuid'] = log['device_sensor_notification_log_uuid']
                        device_notification_log['device_uuid'] = log['device_uuid']
                        device_notification_log['device_name'] = log['device_name']
                        device_notification_log['user_sensor_uuid'] = log['user_sensor_uuid']
                        device_notification_log['user_sensor_name'] = log['user_sensor_name']
                        device_notification_log['threshold_value'] = log['threshold_value']
                        device_notification_log['latest_value'] = log['latest_value']
                        device_notification_log['time_reached'] = log['time_reached']
                        device_notification_log['threshold_direction'] = log['threshold_direction']
                        device_notification_log['unit_symbol'] = log['unit_symbol']
                        device_notification_log['notification_type'] = log['notification_type']
                        data['device_notification_logs'].append(device_notification_log)

                    response_data = rg.data_response_generator(data)
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

                else:
                    response_data = rg.error_response_generator(400, user['error'])
                    return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

    else:
        response_data = rg.error_response_generator(400, 'Bad request method')
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
