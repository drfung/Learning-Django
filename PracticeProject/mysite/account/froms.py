from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,UserInfo

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_passsword2(self):
        cd = self.cleaned_data
        if cd.get("password") != cd.get("password2"):
            raise forms.ValidationError("passwords do not match.")
        return cd.get("password2")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone", "birth"]


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['school','company','address','profession','aboutme','photo']

class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['email',]