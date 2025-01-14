from django import forms
from .models import Announcementss

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcementss
        fields = ['title', 'content', 'date', 'time']
