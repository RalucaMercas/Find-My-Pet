from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumbers import parse, is_valid_number, NumberParseException, region_code_for_country_code

from django.forms.widgets import PasswordInput


class ConfirmPasswordForm(forms.Form):
    password = forms.CharField(widget=PasswordInput(), label="Confirm Your Password")


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your phone number with country code"}),
    )
    country = CountryField().formfield(
        required=True,
        widget=CountrySelectWidget(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "country", "phone_number", "password1", "password2"]

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        country = self.cleaned_data.get("country")

        if not phone or not country:
            raise forms.ValidationError("Both phone number and country are required.")

        try:
            parsed_number = parse(phone, country)

            if not is_valid_number(parsed_number):
                region_code = region_code_for_country_code(parsed_number.country_code)
                if not region_code:
                    raise forms.ValidationError("The country code in the phone number is invalid.")
                elif region_code != country:
                    raise forms.ValidationError(
                        f"The phone number does not match the selected country ({country})."
                    )
                else:
                    raise forms.ValidationError(
                        "The phone number is not valid. Ensure it includes the correct country code and is in the correct format."
                    )

        except NumberParseException as e:
            raise forms.ValidationError(
                f"The phone number format is invalid. Error: {str(e)}"
            )

        return phone


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your phone number with country code"}),
    )
    country = CountryField().formfield(
        required=True,
        widget=CountrySelectWidget(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "country", "phone_number"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "description",
            "pet_name",
            "area",
            "date_lost",
            "pet_type",
            "pet_sex",
            "email",
            "phone_number",
            "reward",
        ]
        widgets = {
            'date_lost': forms.DateInput(attrs={'type': 'date'}),
            'reward': forms.NumberInput(attrs={'placeholder': 'Reward in €'}),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and isinstance(user, User):
            self.fields['email'].initial = user.email
            self.fields['phone_number'].initial = user.phone_number

    def clean_date_lost(self):
        date_lost = self.cleaned_data.get('date_lost')
        if date_lost and date_lost > date.today():
            raise forms.ValidationError("The date cannot be in the future.")
        return date_lost
