from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from user.widgets import ReadOnlyPasswordHashWidget

class ReadOnlyPasswordHashField(forms.Field):
    widget = ReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        # Always return initial because the widget doesn't
        # render an input field.
        return initial

    def has_changed(self, initial, data):
        return False

class UserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'required': 'true', }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'required': 'true', }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone',
                  'password1', 'password2', 'is_staff', 'is_active', 'type')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'Phone'}),
            'type': forms.Select(attrs={'class': 'vTextField form-control'}),
            'is_staff' : forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }
        error_messages = {
            'first_name': {
                'required': "First Name is required",
            },
            'last_name' : {
                 'required': "Last Name is required",
            },
            'email' : {
                 'required': "Email is required",
            }
        }

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        if(type == 1):
            has_hospital = False
            hospital_form_count = int(self.data.get('hospital-TOTAL_FORMS', 0))
            for i in range(0, hospital_form_count):
                try:
                    if self.data.get('hospital-{0}-hospital_name'.format(i), '') == '':
                        has_hospital = True
                except ValueError:
                    pass

            if has_hospital:
                raise ValidationError("Hospital Details is required")

        if(type == 2):
            has_vehicle = False
            vehicle_form_count = int(
                self.data.get('vehicle_set-TOTAL_FORMS', 0))
            for i in range(0, vehicle_form_count):
                try:
                    if self.data.get('vehicle_set-{0}-vehicle_no'.format(i), '') == '':
                        has_vehicle = True
                except ValueError:
                    pass

            if has_vehicle:
                raise ValidationError("Vehicle Details is required")


class UserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Chnage Password"),
        help_text=_(
            "You can change the password using "
            "<a href=\"{}\">this form</a>."
        ),
    )