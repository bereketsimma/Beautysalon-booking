from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Appointment, Service, Staff

from django import forms

# class BookingForm(forms.ModelForm):
#     service = forms.ModelChoiceField(
#         queryset=Service.objects.all(),
#         empty_label="Select Service",
#         widget=forms.Select(attrs={'class': 'form-select'})
#     )
#     stylist = forms.ModelChoiceField(
#         queryset=Stylist.objects.all(),
#         empty_label="Select Stylist",
#         widget=forms.Select(attrs={'class': 'form-select'})
#     )
#     date = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
#     )
#     time = forms.TimeField(
#         widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
#     )

#     class Meta:
#         model = Booking
#         fields = ['service', 'stylist', 'date', 'time']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'staff', 'date', 'time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add bootstrap classes
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        # Optional: limit stylist choices or ordering
        self.fields['staff'].queryset = Staff.objects.all()
        self.fields['service'].queryset = Service.objects.all()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']  # remove password here

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
            label="Username"
        )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            label="Password"
        )
    
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')



