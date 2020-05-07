from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

attrs = {'class': 'form-control'}


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs=attrs))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs=attrs))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs=attrs))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs=attrs))
    password2 = None

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for filename in ['first_name', 'username', 'password1']:
            self.fields[filename].help_text = None


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs=attrs))