from django import forms

from cargos.models import Cargos
from funcionarios.web.forms import (
    CATEGORIA_ESOCIAL_CHOICES,
    VINCULO_EMPREGATICIO_CHOICES,
    _choices_with_current,
)


def _ap_current_field_value(form, field_name):
    value = None
    if form.is_bound:
        value = form.data.get(field_name)
    if value in (None, ""):
        value = form.initial.get(field_name)
    return value


TIPO_CHOICES = (
    ("", "Selecione"),
    ("1", "Funcionario - 1º emprego"),
    ("2", "Funcionario - reemprego/Agente publico"),
)

TIPO_FUNCIONARIO_CHOICES = (
    ("", "Nao informado"),
)

TIPO_CONTRATO_CHOICES = (
    ("", "Nao informado"),
    ("1", "1 - Prazo indeterminado"),
    ("2", "2 - Prazo determinado, definido em dias"),
    ("3", "3 - Prazo determinado, vinculado à ocorrência de um fato"),
)


def _ctrl(placeholder=None, extra=None):
    attrs = {"class": "form-control", "autocomplete": "off"}
    if placeholder:
        attrs["placeholder"] = placeholder
    if extra:
        extra_classes = extra.pop("class", None)
        attrs.update(extra)
        if extra_classes:
            attrs["class"] = f"{attrs.get('class', '')} {extra_classes}".strip()
    return attrs


def _cargo_choices(banco, db_alias):
    choices = [("", "Selecione")]
    try:
        rows = (
            Cargos.objects.using(db_alias)
            .filter(registro=banco)
            .order_by("carg_codi")
            .values_list("carg_codi", "carg_nome")
        )
        for cod, nome in rows:
            if cod is None:
                continue
            desc = str(nome).strip() if nome else ""
            descricao = f"{cod} - {desc}" if desc else f"{cod}"
            choices.append((int(cod), descricao))
    except Exception:
        pass
    return choices


def _cbo_choices(banco, db_alias):
    choices = [("", "Selecione")]
    seen = set()
    try:
        rows = (
            Cargos.objects.using(db_alias)
            .filter(registro=banco)
            .exclude(carg_cbo__isnull=True)
            .exclude(carg_cbo="")
            .order_by("carg_cbo", "carg_nome")
            .values_list("carg_cbo", "carg_nome")
        )
        for valor_cbo, nome_cargo in rows:
            cbo_clean = "".join(ch for ch in str(valor_cbo) if ch.isdigit())[:6]
            if not cbo_clean or cbo_clean in seen:
                continue
            seen.add(cbo_clean)
            desc_ref = (nome_cargo or "").strip()
            descricao = f"{cbo_clean} - {desc_ref}" if desc_ref else cbo_clean
            choices.append((cbo_clean, descricao))
    except Exception:
        pass
    return choices


def _validar_cpf_digitos(digits: str) -> bool:
    if len(digits) != 11:
        return False
    if digits == digits[0] * 11:
        return False

    def _calc_dv(base: str) -> int:
        pesos = list(range(len(base) + 1, 1, -1))
        soma = sum(int(d) * p for d, p in zip(base, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    dv1 = _calc_dv(digits[:9])
    if dv1 != int(digits[9]):
        return False
    dv2 = _calc_dv(digits[:10])
    return dv2 == int(digits[10])


class AdmissaoPreliminarForm(forms.Form):
    empresa = forms.IntegerField(label="Empresa", widget=forms.NumberInput(attrs=_ctrl("Empresa")))
    empresa_nome = forms.CharField(
        label="Nome da empresa",
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs=_ctrl(extra={"readonly": "readonly"})),
    )
    codigo = forms.IntegerField(
        label="Codigo",
        required=False,
        widget=forms.NumberInput(attrs=_ctrl("Codigo")),
    )
    nome = forms.CharField(label="Nome", max_length=120, widget=forms.TextInput(attrs=_ctrl("Nome completo")))
    tipo = forms.ChoiceField(label="Tipo", choices=TIPO_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    codigo_funcionario = forms.CharField(
        label="Cod. funcionário",
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs=_ctrl("Codigo interno")),
    )
    cpf = forms.CharField(
        label="CPF",
        max_length=14,
        widget=forms.TextInput(attrs=_ctrl("000.000.000-00", {"data-mask": "cpf", "inputmode": "numeric"})),
    )
    nis = forms.CharField(
        label="NIS",
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs=_ctrl("000.00000.00-0", {"data-mask": "nis", "inputmode": "numeric"})),
    )
    nascimento = forms.DateField(
        label="Nascimento",
        required=False,
        widget=forms.DateInput(
            attrs=_ctrl(extra={"type": "date", "data-ap-field": "nascimento"}), format="%Y-%m-%d"
        ),
        input_formats=["%Y-%m-%d"],
    )
    admissao = forms.DateField(
        label="Admissao",
        widget=forms.DateInput(
            attrs=_ctrl(extra={"type": "date", "data-ap-field": "admissao"}), format="%Y-%m-%d"
        ),
        input_formats=["%Y-%m-%d"],
    )
    tipo_funcionario = forms.ChoiceField(
        label="Tipo de funcionario",
        required=False,
        choices=TIPO_FUNCIONARIO_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    salario_base = forms.DecimalField(
        label="Salario base",
        required=False,
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(attrs=_ctrl("0,00", {"step": "0.01", "inputmode": "decimal"})),
    )
    matricula_esocial = forms.CharField(
        label="Matricula eSocial",
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs=_ctrl("Matricula")),
    )
    recibo_entrega_esocial = forms.CharField(
        label="Recibo de entrega do eSocial",
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs=_ctrl("Recibo/protocolo")),
    )
    categoria_esocial = forms.TypedChoiceField(
        label="Categoria eSocial",
        required=False,
        coerce=int,
        empty_value=None,
        choices=CATEGORIA_ESOCIAL_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    vinculo_empregaticio = forms.TypedChoiceField(
        label="Vinculo empregaticio",
        required=False,
        coerce=int,
        empty_value=None,
        choices=VINCULO_EMPREGATICIO_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    cargo = forms.TypedChoiceField(
        label="Cargo",
        required=False,
        coerce=int,
        empty_value=None,
        choices=[("", "Selecione")],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    cbo = forms.ChoiceField(
        label="CBO",
        required=False,
        choices=[("", "Selecione")],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    tipo_contrato = forms.ChoiceField(
        label="Tipo de contrato de trabalho",
        required=False,
        choices=TIPO_CONTRATO_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    prazo_experiencia_dias = forms.IntegerField(
        label="Prazo de experiencia (dias)",
        required=False,
        widget=forms.NumberInput(attrs=_ctrl("Dias", {"data-ap-field": "prazo_experiencia_dias"})),
    )
    fim_primeiro_prazo = forms.DateField(
        label="Fim do 1º prazo",
        required=False,
        widget=forms.DateInput(
            attrs=_ctrl(
                extra={
                    "type": "date",
                    "data-ap-field": "fim_primeiro_prazo",
                    "readonly": True,
                    "class": "form-control bg-secondary-subtle",
                }
            ),
            format="%Y-%m-%d",
        ),
        input_formats=["%Y-%m-%d"],
    )

    def __init__(self, *args, empresa_nome="", banco=None, db_alias=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["empresa_nome"].initial = empresa_nome
        self._banco = banco
        self._db_alias = db_alias

        cargo_valor = _ap_current_field_value(self, "cargo")
        self.fields["cargo"].choices = _choices_with_current(
            _cargo_choices(banco, db_alias), cargo_valor
        )

        cbo_valor = _ap_current_field_value(self, "cbo")
        self.fields["cbo"].choices = _choices_with_current(
            _cbo_choices(banco, db_alias), cbo_valor
        )

        vinculo_valor = _ap_current_field_value(self, "vinculo_empregaticio")
        self.fields["vinculo_empregaticio"].choices = _choices_with_current(
            VINCULO_EMPREGATICIO_CHOICES, vinculo_valor
        )

        categoria_valor = _ap_current_field_value(self, "categoria_esocial")
        self.fields["categoria_esocial"].choices = _choices_with_current(
            CATEGORIA_ESOCIAL_CHOICES, categoria_valor
        )

    def clean_cpf(self):
        value = (self.cleaned_data.get("cpf") or "").strip()
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) != 11:
            raise forms.ValidationError("Informe um CPF valido com 11 digitos.")
        if not _validar_cpf_digitos(digits):
            raise forms.ValidationError("CPF informado e invalido (dígitos verificadores nao batem).")
        return digits

    def clean_nis(self):
        value = (self.cleaned_data.get("nis") or "").strip()
        if not value:
            return ""
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) > 11:
            digits = digits[:11]
        if len(digits) not in (0, 11):
            raise forms.ValidationError("Informe um NIS valido com 11 digitos.")
        return digits

    def clean_cbo(self):
        value = (self.cleaned_data.get("cbo") or "").strip()
        return "".join(ch for ch in value if ch.isdigit())[:6]

    def clean(self):
        cleaned = super().clean()
        admissao = cleaned.get("admissao")
        dias = cleaned.get("prazo_experiencia_dias")
        if admissao and dias is not None and dias > 0:
            from datetime import timedelta

            cleaned["fim_primeiro_prazo"] = admissao + timedelta(days=int(dias))
        return cleaned
