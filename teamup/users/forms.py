from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.forms.widgets import HiddenInput

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Set the email field widget to HiddenInput
        self.fields['email'].widget = HiddenInput()

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'sport_1', 'skill_level_1', 'sport_2', 'skill_level_2', 'sport_3', 'skill_level_3', 'location', 'age', 'gender', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        self.fields['latitude'].widget = HiddenInput()
        self.fields['longitude'].widget = HiddenInput()