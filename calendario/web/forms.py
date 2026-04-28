from django import forms

from calendario.models import Calendariorh


class CalendarioEventoForm(forms.ModelForm):
    class Meta:
        model = Calendariorh
        fields = ["cale_cida", "cale_refe", "cale_data", "cale_dia_desc"]
        labels = {
            "cale_cida": "Código",
            "cale_refe": "Referência",
            "cale_data": "Data",
            "cale_dia_desc": "Dia com descanso",
        }
        widgets = {
            "cale_cida": forms.TextInput(attrs={"class": "form-control", "maxlength": "7", "placeholder": "Código do evento"}),
            "cale_refe": forms.TextInput(attrs={"class": "form-control", "maxlength": "7", "placeholder": "AAAAMM"}),
            "cale_data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "cale_dia_desc": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
