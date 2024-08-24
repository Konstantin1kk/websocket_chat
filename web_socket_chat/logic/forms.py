from django import forms
from . import models


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Username:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='First name:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email:', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'email', 'password']


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Username:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
