from django.shortcuts import render, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rumahiot_surat.apps.notification.utils import ResponseGenerator, RequestUtils
from rumahiot_surat.apps.logger.forms import DeviceSensorNotificationForm
from rumahiot_surat.settings import SECRET_KEY

# Create your views here.

# For panel device notification in the top right corner
@csrf_exempt
def device_panel_notification(request):
    # Class import
    rg = ResponseGenerator()
    requtils = RequestUtils()

    if request.method == "POST":
        try:
            token = requtils.get_access_token(request)
        except KeyError:
            response_data = rg.error_response_generator(400, "Please define the authorization header")
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        else:
            if token['token'] is None:
                response_data = rg.error_response_generator(400, token['error'])
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
            else:
                form = DeviceSensorNotificationForm(request.POST)
                if form.is_valid():
                    if token['token'] == SECRET_KEY:
                        data = {
                            'user_uuid': form.cleaned_data['user_uuid'],
                            'device_uuid': form.cleaned_data['device_uuid'],
                            'device_name': form.cleaned_data['device_name'],
                            'user_sensor_uuid': form.cleaned_data['user_sensor_uuid'],
                            'user_sensor_name': form.cleaned_data['user_sensor_name'],
                            'threshold_value': form.cleaned_data['threshold_value'],
                            'latest_value': form.cleaned_data['latest_value'],
                            'time_reached': form.cleaned_data['time_reached'],
                            'threshold_direction': form.cleaned_data['threshold_direction'],
                            'unit_symbol': form.cleaned_data['unit_symbol'],
                            'notification_type': form.cleaned_data['notification_type'],
                            'sent': form.cleaned_data['sent'],
                            'viewed': form.cleaned_data['viewed']
                        }

                        print(data)
                        return HttpResponse("hehe")
                    else:
                        response_data = rg.error_response_generator(400, "Invalid authorization key")
                        return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
                else:
                    response_data = rg.error_response_generator(400, "Invalid or missing parameter submitted")
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

    else:
        response_data = rg.error_response_generator(400, "Bad request method")
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)