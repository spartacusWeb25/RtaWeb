from django import forms
from dependentesrh.models import Dependentesrh
from dependentesrh.web.choices import (
    TIPO_DEPENDENCIA_CHOICES,
    TIPO_DEPENDENTE_CHOICES,
    CIDADES_TOP_BR_CHOICES,
    CIDADES_POR_CODIGO,
    UF_POR_CODIGO_IBGE,
)


class DependentesrhForm(forms.ModelForm):
    class Meta:
        model = Dependentesrh
        fields = (
            'registro',
            'depe_empr',
            'depe_fili',
            'depe_func',
            'depe_codi',
            'depe_nome',
            'depe_nascimento',
            'depe_cpf',
            'depe_matricula',
            'depe_local_nascimento',
            'depe_cidade_codigo',
            'depe_cidade',
            'depe_cartorio',
            'depe_numero_registro',
            'depe_numero_livro',
            'depe_numero_folha',
            'depe_data_entrega',
            'depe_tipo_dependencia',
            'depe_data_baixa',
            'depe_ir_ate',
            'depe_tipo_dependente',
            'depe_invalido',
            'depe_observacoes',
        )
        widgets = {
            'registro': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_empr': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_fili': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_func': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_codi': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'depe_cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_local_nascimento': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_cidade_codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_cartorio': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_numero_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_numero_livro': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_numero_folha': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_data_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'depe_tipo_dependencia': forms.Select(attrs={'class': 'form-select'}),
            'depe_data_baixa': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'depe_ir_ate': forms.TextInput(attrs={'class': 'form-control'}),
            'depe_tipo_dependente': forms.Select(attrs={'class': 'form-select'}),
            'depe_invalido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'depe_observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'registro': 'Registro',
            'depe_empr': 'Empresa',
            'depe_fili': 'Filial',
            'depe_func': 'Funcionário',
            'depe_codi': 'Código',
            'depe_nome': 'Nome',
            'depe_nascimento': 'Data de Nascimento',
            'depe_cpf': 'CPF',
            'depe_matricula': 'Matrícula',
            'depe_local_nascimento': 'Local de Nascimento',
            'depe_cidade_codigo': 'Código da Cidade',
            'depe_cidade': 'Cidade',
            'depe_cartorio': 'Cartório',
            'depe_numero_registro': 'Número de Registro',
            'depe_numero_livro': 'Número do Livro',
            'depe_numero_folha': 'Número da Folha',
            'depe_data_entrega': 'Data de Entrega',
            'depe_tipo_dependencia': 'Tipo de Dependência',
            'depe_data_baixa': 'Data de Baixa',
            'depe_ir_ate': 'IR até',
            'depe_tipo_dependente': 'Tipo de Dependente',
            'depe_invalido': 'Inválido',
            'depe_observacoes': 'Observações',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['registro'].widget = forms.HiddenInput()
        self.fields['registro'].required = False

        self.fields['depe_codi'].required = False
        self.fields['depe_codi'].widget = forms.HiddenInput(
            attrs={'value': self.fields['depe_codi'].initial or ''}
        )

        self.fields['depe_empr'] = forms.TypedChoiceField(
            coerce=lambda v: int(v) if v and str(v).isdigit() else (v or None),
            choices=[('', 'Selecione...')],
            label='Código da Empresa',
            required=True,
            widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_depe_empr'})
        )

        self.fields['depe_fili'] = forms.IntegerField(
            label='Código da Filial',
            required=True,
            min_value=1,
            max_value=9999,
            widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_depe_fili'})
        )

        self.fields['depe_func'] = forms.TypedChoiceField(
            coerce=lambda v: int(v) if v and str(v).isdigit() else (v or None),
            choices=[('', 'Selecione...')],
            label='Código do Funcionário',
            required=True,
            widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_depe_func'})
        )

        self.fields['depe_tipo_dependencia'] = forms.TypedChoiceField(
            coerce=lambda v: int(v) if v and str(v).isdigit() else (v or None),
            choices=TIPO_DEPENDENCIA_CHOICES,
            label='Tipo de Dependência',
            required=False,
            widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_depe_tipo_dependencia'})
        )

        self.fields['depe_tipo_dependente'] = forms.TypedChoiceField(
            coerce=lambda v: int(v) if v and str(v).isdigit() else (v or None),
            choices=TIPO_DEPENDENTE_CHOICES,
            label='Tipo de Dependente',
            required=False,
            widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_depe_tipo_dependente'})
        )

        self.fields['depe_cpf'] = forms.CharField(
            label='CPF',
            required=False,
            max_length=14,
            widget=forms.TextInput(attrs={
                'class': 'form-control mask-cpf',
                'id': 'id_depe_cpf',
                'maxlength': '14',
                'placeholder': '000.000.000-00',
            })
        )

        self.fields['depe_cidade_codigo'] = forms.CharField(
            label='Código da Cidade (IBGE) — digite código ou nome',
            required=False,
            max_length=120,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_depe_cidade_codigo',
                'list': 'dl_cidades_ibge',
                'placeholder': 'Digite o código IBGE ou o nome da cidade/UF...',
                'autocomplete': 'off',
            })
        )

        self.fields['depe_cidade'] = forms.CharField(
            label='Cidade',
            required=False,
            max_length=120,
            widget=forms.HiddenInput(attrs={'id': 'id_depe_cidade'})
        )

        def _limpar_cpf(v):
            return ''.join(ch for ch in str(v or '') if ch.isdigit())[:11]

        cpf_initial_11 = None
        if 'depe_cpf' in self.initial and self.initial.get('depe_cpf'):
            cpf_initial_11 = _limpar_cpf(self.initial['depe_cpf'])
            self.initial['depe_cpf'] = cpf_initial_11 or None
        cpf_data_11 = None
        if self.data and 'depe_cpf' in self.data and self.data.get('depe_cpf'):
            cpf_data_11 = _limpar_cpf(self.data['depe_cpf'])
            _mutable = getattr(self.data, '_mutable', None)
            if _mutable is False:
                try:
                    self.data._mutable = True
                    self.data['depe_cpf'] = cpf_data_11 or self.data.get('depe_cpf', '')
                except Exception:
                    pass
                try:
                    self.data._mutable = False
                except Exception:
                    pass
        if getattr(self, 'instance', None) and getattr(self.instance, 'depe_cpf', None):
            try:
                self.instance.depe_cpf = _limpar_cpf(self.instance.depe_cpf) or None
            except Exception:
                pass

        cod_cidade_initial = self.initial.get('depe_cidade_codigo')
        if cod_cidade_initial not in (None, ''):
            try:
                cod_cidade_num = int(cod_cidade_initial)
            except (TypeError, ValueError):
                cod_cidade_num = None
            if cod_cidade_num is not None:
                par = CIDADES_POR_CODIGO.get(cod_cidade_num)
                if par:
                    nome, uf = par
                    self.initial['depe_cidade_codigo'] = f"{cod_cidade_initial:0>7} — {nome} / {uf}"

    def clean_depe_cpf(self):
        valor = self.cleaned_data.get('depe_cpf') or ''
        apenas_digitos = ''.join(ch for ch in str(valor) if ch.isdigit())
        if len(apenas_digitos) > 11:
            apenas_digitos = apenas_digitos[:11]
        return apenas_digitos or None

    def clean_depe_cidade_codigo(self):
        valor = self.cleaned_data.get('depe_cidade_codigo')
        if valor in (None, ''):
            return None
        valor_str = str(valor).strip()

        match_codigo = None
        apenas_digitos = ''.join(ch for ch in valor_str if ch.isdigit())
        if len(apenas_digitos) >= 2:
            try:
                match_codigo = int(apenas_digitos)
            except (TypeError, ValueError):
                match_codigo = None

        if match_codigo is not None and match_codigo in CIDADES_POR_CODIGO:
            nome, uf = CIDADES_POR_CODIGO[match_codigo]
            self.cleaned_data['depe_cidade'] = f"{nome} / {uf}"
            return match_codigo

        if match_codigo is not None and len(apenas_digitos) == 7:
            codigo_str = f"{match_codigo:07d}"
            try:
                uf_codigo = int(codigo_str[:2])
            except (TypeError, ValueError):
                uf_codigo = None
            if uf_codigo is not None and uf_codigo in UF_POR_CODIGO_IBGE:
                uf_valida = UF_POR_CODIGO_IBGE[uf_codigo]
                self.cleaned_data['depe_cidade'] = f"Cidade / {uf_valida}"
                return match_codigo

        texto_busca = valor_str.lower()
        if texto_busca:
            encontrei_codigo = None
            encontrei_nome = None
            encontrei_uf = None
            for cod_num, (n, u) in CIDADES_POR_CODIGO.items():
                label_1 = f"{cod_num:07d} — {n} / {u}".lower()
                label_2 = f"{n} {u}".lower()
                label_3 = f"{n}/{u}".lower()
                if (texto_busca in label_1) or (texto_busca in label_2) or (texto_busca in label_3):
                    encontrei_codigo = cod_num
                    encontrei_nome = n
                    encontrei_uf = u
                    break
            if encontrei_codigo is not None:
                self.cleaned_data['depe_cidade'] = f"{encontrei_nome} / {encontrei_uf}"
                return encontrei_codigo

        raise forms.ValidationError(
            "Cidade não encontrada. Digite o código IBGE de 7 dígitos "
            "ou comece a digitar o nome/UF e selecione uma opção da lista."
        )

    def clean(self):
        cleaned = super().clean()

        def _to_int_or_none(v):
            if v in (None, '', []):
                return None
            if isinstance(v, int):
                return v
            s = str(v).strip()
            if not s:
                return None
            if s.lstrip('-').isdigit():
                try:
                    return int(s)
                except (TypeError, ValueError):
                    return None
            return None

        for campo in ('depe_empr', 'depe_fili', 'depe_func', 'depe_codi',
                       'depe_cidade_codigo', 'depe_tipo_dependencia', 'depe_tipo_dependente'):
            val = cleaned.get(campo)
            converted = _to_int_or_none(val)
            if converted is None and self.initial and campo in self.initial:
                converted = _to_int_or_none(self.initial.get(campo))
            cleaned[campo] = converted

        return cleaned
