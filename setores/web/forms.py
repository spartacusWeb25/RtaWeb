from django import forms
from setores.models import Setoresrh


class SetoresrhForm(forms.ModelForm):
    class Meta:
        model = Setoresrh
        fields = "__all__"