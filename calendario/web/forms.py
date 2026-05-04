from django import forms
from calendario.models import Calendariorh

class CalendariorhForm(forms.ModelForm):
    class Meta:
        model = Calendariorh
        fields = '__all__'
