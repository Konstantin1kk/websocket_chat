from django import forms
from . import models


class RegisterUserForm(forms.ModelForm):
    first_name = forms.CharField(label='Name:')
    last_name = forms.CharField(label='Last name:')
    email = forms.EmailField(label='Email:')
    password = forms.CharField(label='Password:', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email', 'password']
