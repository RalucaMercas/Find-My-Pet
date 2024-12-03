from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumbers import parse, is_valid_number, NumberParseException


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = PhoneNumberField(required=True)
    country = CountryField().formfield(
        required=True,
        widget=CountrySelectWidget(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "country", "phone_number", "password1", "password2"]