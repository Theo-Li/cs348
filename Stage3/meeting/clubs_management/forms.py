from django import forms
from .models import Meeting

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['date', 'time', 'duration', 'description', 'club', 'room', 'invited_count', 'accepted_count']

from .models import Club, Room

class ReportForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    club = forms.ModelChoiceField(queryset=Club.objects.all(), required=False)
    room = forms.ModelChoiceField(queryset=Room.objects.all(), required=False)
