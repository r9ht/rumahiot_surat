from django import forms


class EmailActivationForm(forms.Form):
    email = forms.EmailField(required=True, max_length=254)
    activation_uuid = forms.CharField(required=True, max_length=254)

class EmailWelcomeForm(forms.Form):
    email = forms.EmailField(required=True, max_length=254)