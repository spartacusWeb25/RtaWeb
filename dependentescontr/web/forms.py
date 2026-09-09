from django import forms
from dependentescontr.models import Dependentescontr
from dependentescontr.choices import (
    TIPO_DEPENDENCIA_CHOICES,
    TIPO_DEPENDENTE_CHOICES,
    GRAU_PARENTESCO_CHOICES,
    CIDADES_TOP_BR_CHOICES,
    CIDADES_POR_CODIGO,
    UF_POR_CODIGO_IBGE,
)


class DependentescontrForm(forms.ModelForm):
    class Meta:
        model = Dependentescontr
        fields = (
            'registro',
            'depecontr_empr',
            'depecontr_fili',
            'depecontr_contr',
            'depecontr_codi',
            'depecontr_nome',
            'depecontr_nascimento',
            'depecontr_cpf',
            'depecontr_matricula',
            'depecontr_local_nascimento',
            'depecontr_cidade_codigo',
            'depecontr_cidade',
            'depecontr_cartorio',
            'depecontr_numero_registro',
            'depecontr_numero_livro',
            'depecontr_numero_folha',
            'depecontr_data_entrega',
            'depecontr_tipo_dependencia',
            'depecontr_data_baixa',
            'depecontr_ir_ate',
            'depecontr_tipo_dependente',
            'depecontr_invalido',
            'depecontr_observacoes',
            'depecontr_grau_parentesco',
            'depecontr_pensao_alimenticia_valor',
            'depecontr_pensao_alimenticia_percentual',
            'depecontr_dependente_irrf',
            'depecontr_dependente_salario_familia',
            'depecontr_rg',
            'depecontr_orgao_emissor_rg',
            'depecontr_uf_rg',
            'depecontr_emissao_rg',
            'depecontr_certidao_nascimento',
            'depecontr_desc_dependencia',
        )
        widgets = {
            'registro': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_empr': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_fili': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_contr': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_codi': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'depecontr_cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_local_nascimento': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_cidade_codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_cartorio': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_numero_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_numero_livro': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_numero_folha': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_data_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'depecontr_tipo_dependencia': forms.Select(attrs={'class': 'form-select'}),
            'depecontr_data_baixa': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'depecontr_ir_ate': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_tipo_dependente': forms.Select(attrs={'class': 'form-select'}),
            'depecontr_invalido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'depecontr_observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'depecontr_grau_parentesco': forms.Select(attrs={'class': 'form-select'}),
            'depecontr_pensao_alimenticia_valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'depecontr_pensao_alimenticia_percentual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'depecontr_dependente_irrf': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'depecontr_dependente_salario_familia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'depecontr_rg': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_orgao_emissor_rg': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_uf_rg': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'depecontr_emissao_rg': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'depecontr_certidao_nascimento': forms.TextInput(attrs={'class': 'form-control'}),
            'depecontr_desc_dependencia': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'registro': 'Registro',
            'depecontr_empr': 'Empresa',
            'depecontr_fili': 'Filial',
            'depecontr_contr': 'Contribuinte',
            'depecontr_codi': 'Código',
            'depecontr_nome': 'Nome do Dependente',
            'depecontr_nascimento': 'Data de Nascimento',
            'depecontr_cpf': 'CPF',
            'depecontr_matricula': 'Matrícula',
            'depecontr_local_nascimento': 'Local de Nascimento',
            'depecontr_cidade_codigo': 'Código da Cidade',
            'depecontr_cidade': 'Cidade',
            'depecontr_cartorio': 'Cartório',
            'depecontr_numero_registro': 'Número de Registro',
            'depecontr_numero_livro': 'Número do Livro',
            'depecontr_numero_folha': 'Número da Folha',
            'depecontr_data_entrega': 'Data de Entrega',
            'depecontr_tipo_dependencia': 'Tipo de Dependência',
            'depecontr_data_baixa': 'Data de Baixa',
            'depecontr_ir_ate': 'IR até',
            'depecontr_tipo_dependente': 'Tipo de Dependente',
            'depecontr_invalido': 'Inválido',
            'depecontr_observacoes': 'Observações',
            'depecontr_grau_parentesco': 'Grau de Parentesco',
            'depecontr_pensao_alimenticia_valor': 'Pensão Alimentícia (Valor R$)',
            'depecontr_pensao_alimenticia_percentual': 'Pensão Alimentícia (% sobre Salário)',
            'depecontr_dependente_irrf': 'Dependente para fins de IRRF',
            'depecontr_dependente_salario_familia': 'Dependente para fins de Salário Família',
            'depecontr_rg': 'RG',
            'depecontr_orgao_emissor_rg': 'Órgão Emissor RG',
            'depecontr_uf_rg': 'UF RG',
            'depecontr_emissao_rg': 'Data de Emissão RG',
            'depecontr_certidao_nascimento': 'Certidão de Nascimento',
            'depecontr_desc_dependencia': 'Descrição da Dependência',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['registro'].widget = forms.HiddenInput()
        self.fields['registro'].required = False

        self.fields['depecontr_codi'].required = False
        self.fields['depecontr_codi'].widget = forms.HiddenInput(
            attrs={'value': self.fields['depecontr_codi'].initial or ''}
        )

        self.fields['depecontr_empr'] = forms.TypedChoiceField(
            coerce=lambda v: int(v) if v and str(v).isdigit() else (v or None),
            choices=[('', 'Selecione...')],
            label='Código da Empresa',
            required=True,
            widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_depecontr_empr'})
        )

        self.fields['depecontr_fili'] = forms.IntegerField(
            label='Código da Filial',
            required=True,
            min_value=1,
            max_value=9999,
            widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_depecontr_fili'})
        )

        self.fields['depecontr_contr'] = forms.TypedChoiceField(
            coerce=lambda v: int(v) if v and str(v).isdigit() else (v or None),
            choices=[('', 'Selecione...')],
            label='Código do Contribuinte',
            required=True,
            widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_depecontr_contr'})
        )

        self.fields['depecontr_tipo_dependencia'] = forms.TypedChoiceField(
            coerce=lambda v: int(v) if v and str(v).isdigit() else (v or None),
            choices=TIPO_DEPENDENCIA_CHOICES,
            label='Tipo de Dependência',
            required=False,
            widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_depecontr_tipo_dependencia'})
        )

        self.fields['depecontr_tipo_dependente'] = forms.TypedChoiceField(
            coerce=lambda v: int(v) if v and str(v).isdigit() else (v or None),
            choices=TIPO_DEPENDENTE_CHOICES,
            label='Tipo de Dependente',
            required=False,
            widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_depecontr_tipo_dependente'})
        )

        self.fields['depecontr_grau_parentesco'] = forms.TypedChoiceField(
            coerce=lambda v: int(v) if v and str(v).isdigit() else (v or None),
            choices=GRAU_PARENTESCO_CHOICES,
            label='Grau de Parentesco',
            required=False,
            widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_depecontr_grau_parentesco'})
        )

        self.fields['depecontr_cpf'] = forms.CharField(
            label='CPF',
            required=False,
            max_length=14,
            widget=forms.TextInput(attrs={
                'class': 'form-control mask-cpf',
                'id': 'id_depecontr_cpf',
                'maxlength': '14',
                'placeholder': '000.000.000-00',
            })
        )

        self.fields['depecontr_cidade_codigo'] = forms.CharField(
            label='Código da Cidade (IBGE) — digite código ou nome',
            required=False,
            max_length=120,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_depecontr_cidade_codigo',
                'list': 'dl_cidades_ibge',
                'placeholder': 'Digite o código IBGE ou o nome da cidade/UF...',
                'autocomplete': 'off',
            })
        )

        self.fields['depecontr_cidade'] = forms.CharField(
            label='Cidade',
            required=False,
            max_length=120,
            widget=forms.HiddenInput(attrs={'id': 'id_depecontr_cidade'})
        )

        def _limpar_cpf(v):
            return ''.join(ch for ch in str(v or '') if ch.isdigit())[:11]

        cpf_initial_11 = None
        if 'depecontr_cpf' in self.initial and self.initial.get('depecontr_cpf'):
            cpf_initial_11 = _limpar_cpf(self.initial['depecontr_cpf'])
            self.initial['depecontr_cpf'] = cpf_initial_11 or None
        cpf_data_11 = None
        if self.data and 'depecontr_cpf' in self.data and self.data.get('depecontr_cpf'):
            cpf_data_11 = _limpar_cpf(self.data['depecontr_cpf'])
            _mutable = getattr(self.data, '_mutable', None)
            if _mutable is False:
                try:
                    self.data._mutable = True
                    self.data['depecontr_cpf'] = cpf_data_11 or self.data.get('depecontr_cpf', '')
                except Exception:
                    pass
                try:
                    self.data._mutable = False
                except Exception:
                    pass
        if getattr(self, 'instance', None) and getattr(self.instance, 'depecontr_cpf', None):
            try:
                self.instance.depecontr_cpf = _limpar_cpf(self.instance.depecontr_cpf) or None
            except Exception:
                pass

        cod_cidade_initial = self.initial.get('depecontr_cidade_codigo')
        if cod_cidade_initial not in (None, ''):
            try:
                cod_cidade_num = int(cod_cidade_initial)
            except (TypeError, ValueError):
                cod_cidade_num = None
            if cod_cidade_num is not None:
                par = CIDADES_POR_CODIGO.get(cod_cidade_num)
                if par:
                    nome, uf = par
                    self.initial['depecontr_cidade_codigo'] = f"{cod_cidade_initial:0>7} — {nome} / {uf}"

    def clean_depecontr_cpf(self):
        valor = self.cleaned_data.get('depecontr_cpf') or ''
        apenas_digitos = ''.join(ch for ch in str(valor) if ch.isdigit())
        if len(apenas_digitos) > 11:
            apenas_digitos = apenas_digitos[:11]
        return apenas_digitos or None

    def clean_depecontr_cidade_codigo(self):
        valor = self.cleaned_data.get('depecontr_cidade_codigo')
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
            self.cleaned_data['depecontr_cidade'] = f"{nome} / {uf}"
            return match_codigo

        if match_codigo is not None and len(apenas_digitos) == 7:
            codigo_str = f"{match_codigo:07d}"
            try:
                uf_codigo = int(codigo_str[:2])
            except (TypeError, ValueError):
                uf_codigo = None
            if uf_codigo is not None and uf_codigo in UF_POR_CODIGO_IBGE:
                uf_valida = UF_POR_CODIGO_IBGE[uf_codigo]
                self.cleaned_data['depecontr_cidade'] = f"Cidade / {uf_valida}"
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
                self.cleaned_data['depecontr_cidade'] = f"{encontrei_nome} / {encontrei_uf}"
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

        for campo in ('depecontr_empr', 'depecontr_fili', 'depecontr_contr', 'depecontr_codi',
                       'depecontr_cidade_codigo', 'depecontr_tipo_dependencia', 'depecontr_tipo_dependente',
                       'depecontr_grau_parentesco'):
            val = cleaned.get(campo)
            converted = _to_int_or_none(val)
            if converted is None and self.initial and campo in self.initial:
                converted = _to_int_or_none(self.initial.get(campo))
            cleaned[campo] = converted

        return cleaned
