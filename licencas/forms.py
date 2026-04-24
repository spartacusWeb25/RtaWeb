from django import forms


class LoginRtaForm(forms.Form):
    registro = forms.CharField(
        label="Docuemento",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite o documento de acesso",
            "autocomplete": "off",
        })
    )

    usuario = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite o usuário",
            "autocomplete": "username",
        })
    )

    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Digite a senha",
            "autocomplete": "current-password",
        })
    )