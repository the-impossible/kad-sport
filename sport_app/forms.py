from django import forms
from sport_app.models import *


class AccountCreationForm(forms.ModelForm):

    email = forms.CharField(help_text='Enter email', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address',
            'type': 'email',
        }
    ))

    name = forms.CharField(help_text='Enter Full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Full name',
            'class': 'form-control',
        }
    ))

    phone = forms.CharField(help_text='Enter Phone number', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Phone number',
            'class': 'form-control',
        }
    ))

    password = forms.CharField(help_text='New Password', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'New Password',
            'type': 'password',
        }
    ))

    password1 = forms.CharField(help_text='Confirm Password', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'type': 'password',
        }
    ))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != None:
            if User.objects.filter(email=email.lower().strip()).exists():
                raise forms.ValidationError('Email Already taken!')

        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')

        print(f"password: {password}")
        print(f"password1: {password1}")

        if password != password1:
            raise forms.ValidationError("New and Confirm Password does not match!")

        if len(password) < 6:
            raise forms.ValidationError("Password is too short!")

        return password1

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        exists = User.objects.filter(phone=phone).exists()

        if exists:
            raise forms.ValidationError("Phone number already exist!")

        return phone


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'phone')
