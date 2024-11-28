from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


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

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        country = self.cleaned_data.get("country")

        # Validate and parse the phone number based on the selected country
        from phonenumbers import parse, is_valid_number, NumberParseException

        try:
            parsed_number = parse(phone, country.alpha_2)  # Country's ISO alpha-2 code
            if not is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid phone number for the selected country.")
        except NumberParseException:
            raise forms.ValidationError("Invalid phone number format.")

        return phone