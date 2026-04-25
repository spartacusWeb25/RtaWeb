from django import forms

from licencas.models import Usuarios


class UsuarioLicencaForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = [
            "usua_nome",
            "usua_login",
            "usua_senh",
            "usua_ativ",
            "usua_grup",
            "super",
            "usua_emai",
        ]
        labels = {
            "usua_nome": "Nome",
            "usua_login": "Login",
            "usua_senh": "Senha",
            "usua_ativ": "Ativo",
            "usua_grup": "Grupo",
            "super": "Super usuário",
            "usua_emai": "E-mail",
        }
        widgets = {
            "usua_nome": forms.TextInput(attrs={"class": "form-control"}),
            "usua_login": forms.TextInput(attrs={"class": "form-control"}),
            "usua_senh": forms.PasswordInput(attrs={"class": "form-control"}, render_value=True),
            "usua_ativ": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "usua_grup": forms.NumberInput(attrs={"class": "form-control"}),
            "super": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "usua_emai": forms.EmailInput(attrs={"class": "form-control"}),
        }
