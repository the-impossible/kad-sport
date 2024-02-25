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


class AdminCreationForm(forms.ModelForm):
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

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'phone', 'picture')

class UpdateAdminForm(forms.ModelForm):

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

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'picture')


class ScreeningForm(forms.ModelForm):

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), required=True, empty_label="(Select gender)", help_text="Select gender", widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    marital_status = forms.ModelChoiceField(queryset=MaritalStatus.objects.all(), required=True, empty_label="(Select marital status)", help_text="Select marital status", widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    age = forms.CharField(help_text='Your age',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number',
        }
    ))

    date_of_birth = forms.CharField(help_text='Date of Birth',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'date',
        }
    ))

    present_weight = forms.CharField(help_text='present_weight in KG',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number',
            'step':'any',
        }
    ))

    present_height = forms.CharField(help_text='present_height in KG',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number',
            'step':'any',
        }
    ))

    soccer_position = forms.ModelChoiceField(queryset=SoccerPosition.objects.all(), empty_label="(Select soccer position)", help_text="Select soccer position", widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    medical_condition = forms.CharField(help_text="(i.e 'Allergies, Asthma, illness, previous injuries etc.')", widget=forms.Textarea(
        attrs={
            'placeholder': 'Enter address',
            'class': 'form-control',
            'rows': 2,
        }
    ))

    present_weakness = forms.CharField(help_text='Your present weakness', widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 2,
        }
    ))

    next_of_kin = forms.CharField(help_text='Your next_of_kin',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'text',
        }
    ))

    relationship_to_next_of_kin = forms.ModelChoiceField(queryset=Relationship.objects.all(), empty_label="(Select relationship to next of kin)", help_text="Select relationship to next of kin", widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    address = forms.CharField(help_text='Enter address', widget=forms.Textarea(
        attrs={
            'placeholder': 'Enter address',
            'class': 'form-control',
            'rows': 2,
        }
    ))


    class Meta:
        model = Screening
        fields = ('gender', 'marital_status', 'age', 'date_of_birth', 'present_weight', 'present_height', 'soccer_position', 'medical_condition', 'present_weakness', 'next_of_kin', 'relationship_to_next_of_kin', 'address')


class ApplyCandidateForm(AdminCreationForm, ScreeningForm, forms.ModelForm):
    class Meta:
        model = Screening
        fields = ('gender', 'marital_status', 'age', 'date_of_birth', 'present_weight', 'present_height', 'soccer_position', 'medical_condition', 'present_weakness', 'next_of_kin', 'relationship_to_next_of_kin', 'address')

class CandidateUpdateForm(forms.ModelForm):
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

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'picture')

