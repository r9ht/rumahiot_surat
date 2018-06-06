from django import forms

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True, max_length=254)
    forgot_password_uuid = forms.CharField(required=True, max_length=32)
    full_name = forms.CharField(required=True, max_length=70)

class EmailActivationForm(forms.Form):
    email = forms.EmailField(required=True, max_length=254)
    activation_uuid = forms.CharField(required=True, max_length=32)
    full_name = forms.CharField(required=True, max_length=70)

class EmailWelcomeForm(forms.Form):
    email = forms.EmailField(required=True, max_length=254)
    full_name = forms.CharField(required=True, max_length=70)

# For submitting notification email
class DeviceNotificationEmail(forms.Form):
    email = forms.EmailField(required=True, max_length=254)
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

    # Todo : add cleaning method for the forms (not urgent, as it will be used directly by other authorized service)
