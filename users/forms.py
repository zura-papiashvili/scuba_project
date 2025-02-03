from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_countries import countries
from .models import User
from django_countries.widgets import CountrySelectWidget


class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    country = forms.ChoiceField(
        widget=CountrySelectWidget(attrs={"class": "form-control"}),
        choices=[(code, name) for code, name in countries],
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",  # Remove 'username' from here
            "password1",
            "password2",
            "birth_date",
            "country",
            "phone_number",
            "biography",
            "address",
        )
        widgets = {
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "biography": forms.Textarea(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]  # Set username as email
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=255)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "biography",
            "profile_picture",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control"}
            )  # Add Bootstrap classes for styling
