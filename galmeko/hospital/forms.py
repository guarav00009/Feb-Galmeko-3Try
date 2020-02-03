from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from hospital.models import Hospital

class CustomHospitalCreationForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['hospital_name', 'registration_no',
                  'address', 'status', 'file']
        widgets = {
            'hospital_name': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'Hospital Name', 'required': 'true', }),
            'registration_no': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'Registration No'}),
            'address': forms.TextInput(attrs={'class': 'vTextField form-control', 'placeholder': 'Address'}),
            'status': forms.Select(attrs={'class': 'vTextField form-control'}),
        }
        error_messages = {
            'registration_no': {
                'required': "Registration no is required",
            },
            'hospital_name': {
                'required': "Hospital Name is required",
            }
        }