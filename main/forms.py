from django import forms


class CredentialsForm(forms.Form):
    client_id = forms.CharField(label='Client ID', max_length=30, min_length=30, required=True)
    # access_token = forms.CharField(label='Access Token', widget=forms.PasswordInput, max_length=30, min_length=30)
    client_secret = forms.CharField(label='Client Secret', widget=forms.PasswordInput, max_length=30, min_length=30, required=True)

    def clean(self):
        cleaned_data = super().clean()
        client_id = cleaned_data.get("client_id")
        # access_token = cleaned_data.get("access_token")
        client_secret = cleaned_data.get("client_secret")

        if not client_id:
            raise forms.ValidationError("Client ID is invalid.")
        # if not access_token:
        #     raise forms.ValidationError("Access Token is invalid.")
        if not client_secret:
            raise forms.ValidationError("Client Secret is invalid.")

        return cleaned_data
