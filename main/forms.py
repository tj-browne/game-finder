from django import forms


class CredentialsForm(forms.Form):
    client_id = forms.CharField(label='Client ID', max_length=30, min_length=30, required=True)
    access_token = forms.CharField(label='Access Token', widget=forms.PasswordInput, max_length=30, min_length=30,
                                   required=True)

    def clean(self):
        cleaned_data = super().clean()
        client_id = cleaned_data.get("client_id")
        access_token = cleaned_data.get("access_token")

        if not client_id or not access_token:
            raise forms.ValidationError("Client ID and Access Token are required.")

        return cleaned_data
