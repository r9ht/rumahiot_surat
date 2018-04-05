from django import forms

# For submitting notification to the panel
class DeviceSensorNotificationForm (forms.Form):
    user_uuid = forms.CharField(required=True, max_length=128)
    user_sensor_uuid = forms.CharField(required=True, max_length=128)
    device_uuid = forms.CharField(required=True, max_length=128)
    device_name = forms.CharField(required=True, max_length=50)
    user_sensor_name = forms.CharField(required=True, max_length=50)
    threshold_value = forms.CharField(required=True, max_length=32)
    latest_value = forms.CharField(required=True, max_length=32)
    time_reached = forms.CharField(required=True, max_length=20)
    # Threshold dirction for inside the email body "1" or "-1"
    threshold_direction = forms.CharField(required=True, max_length=2)
    unit_symbol = forms.CharField(required=True, max_length=10)
    # Notification type : 0 when threshold is reached, and 1 when the value is back to normal
    notification_type = forms.CharField(required=True, max_length=1)
    # sent : 1 (email successfully sent), 0 (email was not sent, or other possible problem)
    sent = forms.CharField(required=True, max_length=1)
    # viewed : 1 (user have seen the notification), 0 (user have not seen the notification)
    viewed = forms.CharField(required=True, max_length=1)

    # Todo : add cleaning method for the forms (not urgent, as it will be used directly by other authorized service)