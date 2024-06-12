from django import forms


class CredentialsForm(forms.Form):
    client_id = forms.CharField(label='Client ID', max_length=255, min_length=1)
    access_token = forms.CharField(label='Access Token', widget=forms.PasswordInput, max_length=255, min_length=1)
