import re
from django import forms
from django.core.validators import MaxLengthValidator
from django.db import models as db_models

from contribuintes.models import Contribuintes
from contribuintes.web.choices import (
    LOGRADOURO_CHOICES,
    TIPO_SANGUINEO_CHOICES,
    ETNIA_RACA_CHOICES,
    SEXO_CHOICES,
    ESTADO_CIVIL_CHOICES,
    GRAU_INSTRUCAO_CHOICES,
    MOTIVO_DESLIGAMENTO_CHOICES,
    INDICATIVO_PENSAO_FGTS_CHOICES,
    TEMPO_RESIDENCIA_CHOICES,
    CONDICAO_INGRESSO_CHOICES,
    CATEGORIA_CNH_CHOICES,
    BANCOS_CHOICES,
    VALID_BANCOS,
    UF_CHOICES,
    CATEGORIA_SEFIP_CHOICES,
    CATEGORIA_ESOCIAL_CHOICES,
    GRAU_RISCO_CHOICES,
    REGIME_PREVIDENCIARIO_CHOICES,
    REGIME_TRABALHISTA_CHOICES,
    CLASSE_CONTRIBUINTE_CHOICES,
    TIPO_VINCULO_EMPREGATICIO_CHOICES,
    NATUREZA_OCUPACAO_CHOICES,
    FORMA_PAGAMENTO_CHOICES,
    TIPO_CONTA_BANCARIA_CHOICES,
    MODO_PAGAMENTO_CHOICES,
    TIPO_ORIGEM_CNPJ_CPF_CHOICES,
    TIPO_DEPENDENTE_CHOICES,
    TIPO_DEPENDENCIA_CHOICES,
    COUNTRY_CHOICES,
    CIDADES_TOP_BR_CHOICES,
    CIDADES_POR_CODIGO,
    PAISES_POR_CODIGO,
    _choices_with_current,
    _current_field_value,
)


def _only_digits(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _cpf_valido(value):
    digits = _only_digits(value)
    if len(digits) != 11 or digits == digits[0] * 11:
        return False

    soma = sum(int(digits[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito_1 = 0 if resto == 10 else resto
    if digito_1 != int(digits[9]):
        return False

    soma = sum(int(digits[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito_2 = 0 if resto == 10 else resto
    return digito_2 == int(digits[10])


COMBO_CHOICES_FIELDS = {
    "contr_logr": LOGRADOURO_CHOICES,
    "contr_tipo_sanguineo": TIPO_SANGUINEO_CHOICES,
    "contr_etnia_raca": ETNIA_RACA_CHOICES,
    "contr_sexo": SEXO_CHOICES,
    "contr_estado_civil": ESTADO_CIVIL_CHOICES,
    "contr_grau_instrucao": GRAU_INSTRUCAO_CHOICES,
    "contr_motivo_desligamento": MOTIVO_DESLIGAMENTO_CHOICES,
    "contr_esocial_indicativo_pensao_alimenticia_fgts": INDICATIVO_PENSAO_FGTS_CHOICES,
    "contr_tempo_residencia": TEMPO_RESIDENCIA_CHOICES,
    "contr_condicao_ingresso": CONDICAO_INGRESSO_CHOICES,
    "contr_ende_uf": UF_CHOICES,
    "contr_uf_rg": UF_CHOICES,
    "contr_uf_carteira_trabalho": UF_CHOICES,
    "contr_uf_cnh": UF_CHOICES,
    "contr_naturalidade": UF_CHOICES,
    "contr_categoria_sefip": CATEGORIA_SEFIP_CHOICES,
    "contr_categoria_esocial": CATEGORIA_ESOCIAL_CHOICES,
    "contr_grau_risco": GRAU_RISCO_CHOICES,
    "contr_regime_previdenciario": REGIME_PREVIDENCIARIO_CHOICES,
    "contr_regime_previdenciario_origem": REGIME_PREVIDENCIARIO_CHOICES,
    "contr_regime_trabalhista": REGIME_TRABALHISTA_CHOICES,
    "contr_classe": CLASSE_CONTRIBUINTE_CHOICES,
    "contr_vinculo_empregaticio": TIPO_VINCULO_EMPREGATICIO_CHOICES,
    "contr_natureza_ocupacao": NATUREZA_OCUPACAO_CHOICES,
    "contr_forma_pagamento": FORMA_PAGAMENTO_CHOICES,
    "contr_tipo_conta": TIPO_CONTA_BANCARIA_CHOICES,
    "contr_modo_pagamento": MODO_PAGAMENTO_CHOICES,
    "contr_tipo_cnpj_cpf_origem": TIPO_ORIGEM_CNPJ_CPF_CHOICES,
    "contr_categoria_origem": CATEGORIA_SEFIP_CHOICES,
    "contr_categoria_cnh": CATEGORIA_CNH_CHOICES,
    "contr_tipo_dependente": TIPO_DEPENDENTE_CHOICES,
    "contr_tipo_dependencia": TIPO_DEPENDENCIA_CHOICES,
}

RADIO_CHOICES = {
    "contr_tipo_cnpj_cpf_origem": TIPO_ORIGEM_CNPJ_CPF_CHOICES,
}


FIELD_LABELS = {
    "registro": "Registro",
    "contr_empr": "Empresa",
    "contr_fili": "Filial",
    "contr_codi": "Código",
    "contr_nome": "Nome",
    "contr_email": "E-mail",
    "contr_cep": "CEP",
    "contr_logr": "Logradouro",
    "contr_ende": "Endereço",
    "contr_ende_nume": "Número",
    "contr_ende_comp": "Complemento",
    "contr_ende_bair": "Bairro",
    "contr_ende_cida_codi": "Cidade (Código IBGE)",
    "contr_ende_cida_desc": "Cidade",
    "contr_ende_uf": "UF",
    "contr_ddd": "DDD",
    "contr_telefone": "Telefone",
    "contr_ddd_celular": "DDD",
    "contr_celular": "Celular",
    "contr_matricula_esocial": "Matrícula eSocial",
    "contr_admissao_preliminar": "Código da admissão preliminar",
    "contr_residencia_exterior": "Residência no exterior",
    "contr_pais_residencia_codi": "País de residência (código)",
    "contr_pais_residencia_desc": "País de residência",
    "contr_cpf": "CPF",
    "contr_rg": "RG",
    "contr_orgao_emissor_rg": "Órgão emissor RG",
    "contr_uf_rg": "UF RG",
    "contr_emissao_rg": "Emissão RG",
    "contr_nis": "NIS / PIS / PASEP",
    "contr_emissao_nis": "Emissão PIS/NIS",
    "contr_titulo_eleitor": "Título de eleitor",
    "contr_zona_titulo": "Zona eleitoral",
    "contr_secao_titulo": "Seção eleitoral",
    "contr_carteira_trabalho": "Carteira de trabalho",
    "contr_serie_carteira_trabalho": "Série CTPS",
    "contr_digito_serie_carteira_trabalho": "Dígito série",
    "contr_uf_carteira_trabalho": "UF CTPS",
    "contr_emissao_carteira_trabalho": "Emissão CTPS",
    "contr_cnh": "CNH",
    "contr_categoria_cnh": "Categoria CNH",
    "contr_uf_cnh": "UF CNH",
    "contr_emissao_cnh": "Emissão CNH",
    "contr_vencimento_cnh": "Vencimento CNH",
    "contr_primeira_habilitacao": "Primeira habilitação",
    "contr_certificado_reservista": "Certificado de reservista",
    "contr_nome_pai": "Nome do pai",
    "contr_nome_mae": "Nome da mãe",
    "contr_nascimento": "Data de nascimento",
    "contr_pais_nascimento_codi": "País de nascimento (código)",
    "contr_pais_nascimento_desc": "País de nascimento",
    "contr_cidade_nascimento_codi": "Cidade de nascimento (código)",
    "contr_cidade_nascimento_desc": "Cidade de nascimento",
    "contr_naturalidade": "Naturalidade (UF)",
    "contr_tipo_sanguineo": "Tipo sanguíneo",
    "contr_etnia_raca": "Etnia / Raça",
    "contr_sexo": "Sexo",
    "contr_estado_civil": "Estado civil",
    "contr_grau_instrucao": "Grau de instrução",
    "contr_pessoa_com_deficiencia": "Pessoa com deficiência",
    "contr_deficiencia_fisica": "Deficiência física",
    "contr_deficiencia_visual": "Deficiência visual",
    "contr_deficiencia_auditiva": "Deficiência auditiva",
    "contr_deficiencia_mental": "Deficiência mental",
    "contr_deficiencia_intelectual": "Deficiência intelectual",
    "contr_reabilitado": "Reabilitado",
    "contr_observacoes_deficiencias": "Observações deficiências",
    "contr_admissao": "Admissão",
    "contr_cadastro": "Cadastro",
    "contr_data_saida": "Data de saída",
    "contr_motivo_desligamento": "Motivo do desligamento",
    "contr_tempo_residencia": "Tempo de residência",
    "contr_condicao_ingresso": "Condição de ingresso",
    "contr_esocial_indicativo_pensao_alimenticia_fgts": "Indicativo",
    "contr_foto_3x4": "Foto 3x4",
    "contr_carteira_identidade_arquivo": "Carteira de identidade (arquivo)",
    "contr_observacoes": "Observações",
    "contr_inativo": "Inativo",
    "contr_tem_dependentes": "Tem dependentes",
    "contr_categoria_sefip": "Categoria Sefip",
    "contr_categoria_esocial": "Categoria eSocial (código)",
    "contr_categoria_esocial_desc": "Categoria eSocial (descrição)",
    "contr_transp_autonomo_contribuicao_inss": "Transport. autônomo % contrib. INSS",
    "contr_percentual_contr_ir": "% contribuição IR",
    "contr_data_opcao": "Data opção",
    "contr_percentual_fgts": "% FGTS",
    "contr_grau_risco": "Grau de risco",
    "contr_rat_aposentadoria": "RAT aposentadoria (%)",
    "contr_descontar_iss": "Descontar ISS",
    "contr_percentual_iss": "% ISS",
    "contr_regime_previdenciario": "Regime previdenciário",
    "contr_categoria_origem": "Categoria Origem",
    "contr_tipo_cnpj_cpf_origem": "Tipo CNPJ/CPF Origem",
    "contr_cnpj_cpf_origem": "CNPJ/CPF Origem",
    "contr_admissao_origem": "Admissão Origem",
    "contr_matricula_origem": "Matrícula Origem",
    "contr_regime_previdenciario_origem": "Regime Previdenciário Origem",
    "contr_classe": "Classe",
    "contr_vinculo_empregaticio": "Vínculo empregatício (código)",
    "contr_vinculo_empregaticio_desc": "Vínculo empregatício (descrição)",
    "contr_depto": "Departamento (código)",
    "contr_depto_desc": "Departamento (descrição)",
    "contr_ccusto": "Centro de custo (código)",
    "contr_ccusto_desc": "Centro de custo (descrição)",
    "contr_cargo": "Cargo (código)",
    "contr_cargo_desc": "Cargo (descrição)",
    "contr_cbo": "CBO (código)",
    "contr_cbo_desc": "CBO (descrição)",
    "contr_natureza_ocupacao": "Natureza de ocupação",
    "contr_orgao_classe": "Órgão de classe ativo",
    "contr_inscricao_orgao_classe": "Inscrição no órgão de classe",
    "contr_orgao_uf_emissao_orgao_classe": "Órgão e UF de emissão",
    "contr_emissao_orgao_classe": "Emissão órgão de classe",
    "contr_validade_orgao_classe": "Validade órgão de classe",
    "contr_forma_pagamento": "Forma de pagamento",
    "contr_remuneracao": "Remuneração",
    "contr_nao_arredondar": "Não arredondar",
    "contr_descontar_inss_do_ir": "Descontar INSS do IR",
    "contr_adiantamento": "Adiantamento",
    "contr_valor_previdencia_privada": "Valor previdência privada",
    "contr_valor_previdencia_privada_13": "Valor previdência privada (13º)",
    "contr_aplica_deducao_mais_benefica_irrf": "Aplica dedução mais benéfica no IRRF",
    "contr_base_inss_multiplos_vinculos": "Base INSS múltiplos vínculos",
    "contr_valor_inss_multiplos_vinculos": "Valor INSS múltiplos vínculos",
    "contr_base_ir_multiplos_vinculos": "Base IR múltiplos vínculos",
    "contr_valor_ir_multiplos_vinculos": "Valor IR múltiplos vínculos",
    "contr_base_inss_multiplos_vinculos_13": "Base INSS múltiplos vínculos (13º)",
    "contr_valor_inss_multiplos_vinculos_13": "Valor INSS múltiplos vínculos (13º)",
    "contr_base_ir_multiplos_vinculos_13": "Base IR múltiplos vínculos (13º)",
    "contr_valor_ir_multiplos_vinculos_13": "Valor IR múltiplos vínculos (13º)",
    "contr_banco": "Banco",
    "contr_banco_desc": "Banco (descrição)",
    "contr_conta_corrente": "Conta corrente",
    "contr_digito_conta_corrente": "Dígito da conta",
    "contr_tipo_conta": "Tipo de conta",
    "contr_modo_pagamento": "Modo de pagamento",
    # ------------------------------------------------------------------
    # NOVOS labels (campos que existem NO BANCO, adicionados na model agora)
    # ------------------------------------------------------------------
    # ABA 1 Cadastrais - Residência exterior
    "contr_ende_exterior": "Endereço",
    "contr_ende_exterior_nume": "Número",
    "contr_ende_exterior_comp": "Complemento",
    "contr_ende_exterior_bair": "Bairro",
    "contr_ende_exterior_cidade": "Cidade",
    "contr_ende_exterior_codigo_postal": "CEP/Código postal",
    # ABA 3 Histórico
    "contr_inicio_adicional_tempo_servico": "Início adicional tempo serviço",
    "contr_data_pagamento_baixa": "Data pagamento baixa",
    "contr_pensao_fgts_valor": "Pensão FGTS (valor)",
    "contr_pensao_fgts_percentual": "Pensão FGTS (%)",
    # ABA 4 Estrangeiro
    "contr_pais_nacionalidade_codi": "País nacionalidade (código)",
    "contr_pais_nacionalidade_desc": "País nacionalidade",
    "contr_chegada_brasil": "Data de chegada ao Brasil",
    "contr_casado_brasileiro": "Casado(a) com brasileiro(a)",
    "contr_tem_filhos_brasileiros": "Tem filhos brasileiros",
    "contr_rne": "RNE",
    "contr_orgao_uf_emissao_rne": "Órgão e UF emissor RNE",
    "contr_emissao_rne": "Data emissão RNE",
    # ABA 5 Documentos
    "contr_aviso_carteira_trabalho_digital": "Aviso CTPS digital",
    "contr_esocial_qualif_status": "Status da qualificação cadastral",
    "contr_esocial_qualif_mensagem": "Mensagem da qualificação",
    "contr_esocial_qualif_data_hora": "Consulta efetuada em",
    "contr_esocial_integrado": "Integrado no eSocial",
    "contr_esocial_integra_data_hora": "Integrado em (data/hora)",
    "contr_esocial_integra_numero_recibo": "Número do recibo",
}


class ContribuinteForm(forms.ModelForm):

    contr_foto_3x4 = forms.FileField(
        required=False,
        label="Foto 3x4",
        widget=forms.ClearableFileInput(attrs={"accept": "image/*", "class": "form-control"}),
    )

    contr_carteira_identidade_arquivo = forms.FileField(
        required=False,
        label="Upload Carteira de Identidade",
        widget=forms.ClearableFileInput(attrs={"accept": "image/*", "class": "form-control"}),
    )

    class Meta:
        model = Contribuintes
        fields = "__all__"
        labels = FIELD_LABELS

    def __init__(self, *args, **kwargs):
        self.db_alias = kwargs.pop("db_alias", None)
        self.banco = kwargs.pop("banco", None)
        super().__init__(*args, **kwargs)

        for nome, field in self.fields.items():
            try:
                model_field = self._meta.model._meta.get_field(nome)
            except Exception:
                model_field = None

            if model_field is not None and isinstance(model_field, db_models.BooleanField):
                field.required = False
                field.widget = forms.CheckboxInput(attrs={"class": "form-check-input"})
                continue

            if model_field is not None and isinstance(model_field, db_models.DateTimeField):
                field.widget = forms.DateTimeInput(
                    attrs={"class": "form-control", "type": "datetime-local"},
                    format="%Y-%m-%dT%H:%M",
                )
                field.input_formats = ["%Y-%m-%dT%H:%M"]
                continue

            if model_field is not None and isinstance(model_field, db_models.DateField):
                field.widget = forms.DateInput(
                    attrs={"class": "form-control", "placeholder": "dd/mm/aaaa", "type": "date"},
                    format="%Y-%m-%d",
                )
                field.input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
                continue

            if model_field is not None and isinstance(model_field, db_models.TextField):
                field.widget.attrs.setdefault("class", "form-control")
                field.widget.attrs.setdefault("rows", 3)
                continue

            if nome in COMBO_CHOICES_FIELDS:
                valor_atual = _current_field_value(self, nome)
                field.widget = forms.Select(
                    attrs={"class": "form-select"},
                    choices=_choices_with_current(COMBO_CHOICES_FIELDS[nome], valor_atual),
                )
                field.required = False
                continue

            if model_field is not None and isinstance(model_field, (db_models.IntegerField, db_models.DecimalField, db_models.FloatField)):
                widget = field.widget
                if not isinstance(widget, forms.NumberInput):
                    widget = forms.NumberInput()
                    field.widget = widget
                widget.attrs["class"] = "form-control"
                if isinstance(model_field, db_models.DecimalField):
                    widget.attrs.setdefault("step", "0.01")
                continue

            if model_field is not None and isinstance(model_field, db_models.BinaryField):
                field.required = False
                field.widget = forms.FileInput(attrs={"class": "form-control", "accept": "image/*"})
                continue

            if nome in RADIO_CHOICES:
                valor_atual = _current_field_value(self, nome)
                field.widget = forms.RadioSelect(
                    choices=_choices_with_current(RADIO_CHOICES[nome], valor_atual),
                    attrs={"class": "form-check-input"},
                )
                field.required = False
                continue

            if nome in COMBO_CHOICES_FIELDS:
                valor_atual = _current_field_value(self, nome)
                field.widget = forms.Select(
                    attrs={"class": "form-select"},
                    choices=_choices_with_current(COMBO_CHOICES_FIELDS[nome], valor_atual),
                )
                field.required = False
                continue

            if not field.widget.attrs.get("class"):
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs.setdefault("class", "form-control")

        if "contr_cpf" in self.fields:
            field = self.fields["contr_cpf"]
            field.max_length = 14
            field.widget.attrs["maxlength"] = 14
            field.widget.attrs["data-mask"] = "cpf"
            field.widget.attrs["inputmode"] = "numeric"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "contr_cep" in self.fields:
            field = self.fields["contr_cep"]
            field.max_length = 9
            field.widget.attrs["maxlength"] = 9
            field.widget.attrs["data-mask"] = "cep"
            field.widget.attrs["inputmode"] = "numeric"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "contr_nis" in self.fields:
            field = self.fields["contr_nis"]
            field.max_length = 14
            field.widget.attrs["maxlength"] = 14
            field.widget.attrs["data-mask"] = "nis"
            field.widget.attrs["inputmode"] = "numeric"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "contr_rg" in self.fields:
            field = self.fields["contr_rg"]
            field.widget.attrs["data-mask"] = "rg"
            field.widget.attrs["inputmode"] = "numeric"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "contr_carteira_trabalho" in self.fields:
            field = self.fields["contr_carteira_trabalho"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "contr_serie_carteira_trabalho" in self.fields:
            field = self.fields["contr_serie_carteira_trabalho"]
            field.max_length = 10
            field.widget.attrs["maxlength"] = 10
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "contr_digito_serie_carteira_trabalho" in self.fields:
            field = self.fields["contr_digito_serie_carteira_trabalho"]
            field.max_length = 2
            field.widget.attrs["maxlength"] = 2
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "contr_uf_carteira_trabalho" in self.fields:
            field = self.fields["contr_uf_carteira_trabalho"]
            field.widget.attrs["style"] = "text-transform: uppercase;"
            field.required = False

        if "contr_cnh" in self.fields:
            field = self.fields["contr_cnh"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "contr_categoria_cnh" in self.fields:
            valor_atual = _current_field_value(self, "contr_categoria_cnh")
            self.fields["contr_categoria_cnh"].choices = _choices_with_current(
                CATEGORIA_CNH_CHOICES, valor_atual
            )
            self.fields["contr_categoria_cnh"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(CATEGORIA_CNH_CHOICES, valor_atual),
            )
            self.fields["contr_categoria_cnh"].required = False

        if "contr_uf_cnh" in self.fields:
            field = self.fields["contr_uf_cnh"]
            field.widget.attrs["style"] = "text-transform: uppercase;"
            field.required = False

        if "contr_titulo_eleitor" in self.fields:
            field = self.fields["contr_titulo_eleitor"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "contr_zona_titulo" in self.fields:
            field = self.fields["contr_zona_titulo"]
            field.max_length = 5
            field.widget.attrs["maxlength"] = 5
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "contr_secao_titulo" in self.fields:
            field = self.fields["contr_secao_titulo"]
            field.max_length = 5
            field.widget.attrs["maxlength"] = 5
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "contr_certificado_reservista" in self.fields:
            field = self.fields["contr_certificado_reservista"]
            field.max_length = 30
            field.widget.attrs["maxlength"] = 30
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "contr_rne" in self.fields:
            field = self.fields["contr_rne"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "contr_cbo" in self.fields:
            field = self.fields["contr_cbo"]
            field.max_length = 10
            field.widget.attrs["maxlength"] = 10
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "contr_ddd" in self.fields:
            field = self.fields["contr_ddd"]
            field.max_length = 2
            field.widget.attrs["maxlength"] = 2
            field.widget.attrs["data-mask"] = "ddd"
            field.widget.attrs["inputmode"] = "numeric"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "contr_ddd_celular" in self.fields:
            field = self.fields["contr_ddd_celular"]
            field.max_length = 2
            field.widget.attrs["maxlength"] = 2
            field.widget.attrs["data-mask"] = "ddd"
            field.widget.attrs["inputmode"] = "numeric"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "contr_telefone" in self.fields:
            field = self.fields["contr_telefone"]
            field.max_length = 9
            field.widget.attrs["maxlength"] = 9
            field.widget.attrs["data-mask"] = "telefone"
            field.widget.attrs["inputmode"] = "numeric"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "contr_celular" in self.fields:
            field = self.fields["contr_celular"]
            field.max_length = 11
            field.widget.attrs["maxlength"] = 15
            field.widget.attrs["data-mask"] = "celular"
            field.widget.attrs["inputmode"] = "numeric"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "contr_cnpj_cpf_origem" in self.fields:
            field = self.fields["contr_cnpj_cpf_origem"]
            field.max_length = 18
            field.widget.attrs["maxlength"] = 18
            field.widget.attrs["data-mask"] = "cnpj_cpf"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "CNPJ ou CPF"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "contr_matricula_origem" in self.fields:
            self.fields["contr_matricula_origem"].required = False

        if "contr_categoria_esocial" in self.fields:
            valor_atual = _current_field_value(self, "contr_categoria_esocial")
            self.fields["contr_categoria_esocial"].label = "Categoria eSocial"
            self.fields["contr_categoria_esocial"].choices = _choices_with_current(
                CATEGORIA_ESOCIAL_CHOICES, valor_atual
            )
            self.fields["contr_categoria_esocial"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(CATEGORIA_ESOCIAL_CHOICES, valor_atual),
            )
            self.fields["contr_categoria_esocial"].required = False

        if "contr_categoria_esocial_desc" in self.fields:
            self.fields["contr_categoria_esocial_desc"].widget = forms.HiddenInput()
            self.fields["contr_categoria_esocial_desc"].required = False

        if "contr_vinculo_empregaticio" in self.fields:
            valor_atual = _current_field_value(self, "contr_vinculo_empregaticio")
            self.fields["contr_vinculo_empregaticio"].label = "Vínculo empregatício"
            self.fields["contr_vinculo_empregaticio"].choices = _choices_with_current(
                TIPO_VINCULO_EMPREGATICIO_CHOICES, valor_atual
            )
            self.fields["contr_vinculo_empregaticio"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(TIPO_VINCULO_EMPREGATICIO_CHOICES, valor_atual),
            )
            self.fields["contr_vinculo_empregaticio"].required = False

        if "contr_vinculo_empregaticio_desc" in self.fields:
            self.fields["contr_vinculo_empregaticio_desc"].widget = forms.HiddenInput()
            self.fields["contr_vinculo_empregaticio_desc"].required = False
            self.fields["contr_vinculo_empregaticio_desc"].validators = [
                v for v in self.fields["contr_vinculo_empregaticio_desc"].validators
                if not isinstance(v, MaxLengthValidator)
            ]

        if "contr_depto" in self.fields:
            valor_atual = _current_field_value(self, "contr_depto")
            self.fields["contr_depto"].label = "Departamento"
            self.fields["contr_depto"].choices = _choices_with_current(
                (("", "Selecione"),), valor_atual
            )
            self.fields["contr_depto"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current((("", "Selecione"),), valor_atual),
            )
            self.fields["contr_depto"].required = False

        if "contr_depto_desc" in self.fields:
            self.fields["contr_depto_desc"].widget = forms.HiddenInput()
            self.fields["contr_depto_desc"].required = False
            self.fields["contr_depto_desc"].validators = [
                v for v in self.fields["contr_depto_desc"].validators
                if not isinstance(v, MaxLengthValidator)
            ]

        if "contr_ccusto" in self.fields:
            valor_atual = _current_field_value(self, "contr_ccusto")
            self.fields["contr_ccusto"].label = "Centro de custo"
            self.fields["contr_ccusto"].choices = _choices_with_current(
                (("", "Selecione"),), valor_atual
            )
            self.fields["contr_ccusto"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current((("", "Selecione"),), valor_atual),
            )
            self.fields["contr_ccusto"].required = False

        if "contr_ccusto_desc" in self.fields:
            self.fields["contr_ccusto_desc"].widget = forms.HiddenInput()
            self.fields["contr_ccusto_desc"].required = False
            self.fields["contr_ccusto_desc"].validators = [
                v for v in self.fields["contr_ccusto_desc"].validators
                if not isinstance(v, MaxLengthValidator)
            ]

        if "contr_cargo" in self.fields:
            valor_atual = _current_field_value(self, "contr_cargo")
            self.fields["contr_cargo"].label = "Cargo"
            self.fields["contr_cargo"].choices = _choices_with_current(
                (("", "Selecione"),), valor_atual
            )
            self.fields["contr_cargo"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current((("", "Selecione"),), valor_atual),
            )
            self.fields["contr_cargo"].required = False

        if "contr_cargo_desc" in self.fields:
            self.fields["contr_cargo_desc"].widget = forms.HiddenInput()
            self.fields["contr_cargo_desc"].required = False
            self.fields["contr_cargo_desc"].validators = [
                v for v in self.fields["contr_cargo_desc"].validators
                if not isinstance(v, MaxLengthValidator)
            ]

        if "contr_cbo" in self.fields:
            valor_atual = _current_field_value(self, "contr_cbo")
            self.fields["contr_cbo"].label = "CBO"
            self.fields["contr_cbo"].choices = _choices_with_current(
                (("", "Selecione"),), valor_atual
            )
            self.fields["contr_cbo"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current((("", "Selecione"),), valor_atual),
            )
            self.fields["contr_cbo"].required = False
            self.fields["contr_cbo"].validators = [
                v for v in self.fields["contr_cbo"].validators
                if not isinstance(v, MaxLengthValidator)
            ]

        if "contr_cbo_desc" in self.fields:
            self.fields["contr_cbo_desc"].widget = forms.HiddenInput()
            self.fields["contr_cbo_desc"].required = False
            self.fields["contr_cbo_desc"].validators = [
                v for v in self.fields["contr_cbo_desc"].validators
                if not isinstance(v, MaxLengthValidator)
            ]

        if "contr_banco" in self.fields:
            field = self.fields["contr_banco"]
            field.required = False
            field.label = "Banco"
            _val = _current_field_value(self, "contr_banco")
            field.widget = forms.Select(
                choices=_choices_with_current(BANCOS_CHOICES, _val),
                attrs={"class": "form-select form-select-md contribuinte-select"},
            )

        if "contr_banco_desc" in self.fields:
            self.fields["contr_banco_desc"].widget = forms.HiddenInput()
            self.fields["contr_banco_desc"].required = False
            self.fields["contr_banco_desc"].validators = [
                v for v in self.fields["contr_banco_desc"].validators
                if not isinstance(v, MaxLengthValidator)
            ]

        if "contr_digito_conta_corrente" in self.fields:
            self.fields["contr_digito_conta_corrente"].required = False
            self.fields["contr_digito_conta_corrente"].widget.attrs["maxlength"] = 5
            self.fields["contr_digito_conta_corrente"].widget.attrs["style"] = "max-width: 120px;"

        if "registro" in self.fields:
            self.fields["registro"].widget = forms.HiddenInput()
            self.fields["registro"].required = False

        if "contr_tem_dependentes" in self.fields:
            self.fields["contr_tem_dependentes"].widget = forms.HiddenInput()
            self.fields["contr_tem_dependentes"].required = False

        if "contr_pais_residencia_codi" in self.fields:
            valor_atual = _current_field_value(self, "contr_pais_residencia_codi")
            self.fields["contr_pais_residencia_codi"].label = "País de residência"
            self.fields["contr_pais_residencia_codi"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(COUNTRY_CHOICES, valor_atual),
            )
            self.fields["contr_pais_residencia_codi"].required = False

        if "contr_pais_residencia_desc" in self.fields:
            self.fields["contr_pais_residencia_desc"].widget = forms.HiddenInput()
            self.fields["contr_pais_residencia_desc"].required = False

        if "contr_residencia_exterior" in self.fields:
            self.fields["contr_residencia_exterior"].widget = forms.HiddenInput()
            self.fields["contr_residencia_exterior"].required = False

        if "contr_pais_nascimento_codi" in self.fields:
            valor_atual = _current_field_value(self, "contr_pais_nascimento_codi")
            self.fields["contr_pais_nascimento_codi"] = forms.CharField(
                label="País de nascimento (código)",
                required=False,
                max_length=120,
                widget=forms.TextInput(attrs={
                    "class": "form-control",
                    "list": "dl_paises_esocial",
                    "placeholder": "Digite o código ou nome do país...",
                    "autocomplete": "off",
                })
            )
            if valor_atual not in (None, ""):
                try:
                    cod_num = int(valor_atual)
                    label = PAISES_POR_CODIGO.get(cod_num)
                    if label:
                        self.initial["contr_pais_nascimento_codi"] = label
                    else:
                        self.initial["contr_pais_nascimento_codi"] = f"{str(cod_num).zfill(3)} - {cod_num}"
                except (TypeError, ValueError):
                    pass

        if "contr_pais_nascimento_desc" in self.fields:
            self.fields["contr_pais_nascimento_desc"].widget = forms.HiddenInput()
            self.fields["contr_pais_nascimento_desc"].required = False

        if "contr_cidade_nascimento_codi" in self.fields:
            valor_atual = _current_field_value(self, "contr_cidade_nascimento_codi")
            self.fields["contr_cidade_nascimento_codi"] = forms.CharField(
                label="Cidade de nascimento (código)",
                required=False,
                max_length=160,
                widget=forms.TextInput(attrs={
                    "class": "form-control",
                    "list": "dl_cidades_ibge",
                    "placeholder": "Digite o código IBGE ou o nome da cidade/UF...",
                    "autocomplete": "off",
                })
            )
            if valor_atual not in (None, ""):
                try:
                    cod_num = int(valor_atual)
                    par = CIDADES_POR_CODIGO.get(cod_num)
                    if par:
                        nome, uf = par
                        self.initial["contr_cidade_nascimento_codi"] = f"{cod_num:07d} — {nome} / {uf}"
                    else:
                        self.initial["contr_cidade_nascimento_codi"] = f"{cod_num:07d} — {cod_num}"
                except (TypeError, ValueError):
                    pass

        if "contr_pais_nacionalidade_codi" in self.fields:
            valor_atual = _current_field_value(self, "contr_pais_nacionalidade_codi")
            self.fields["contr_pais_nacionalidade_codi"].label = "País nacionalidade"
            self.fields["contr_pais_nacionalidade_codi"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(COUNTRY_CHOICES, valor_atual),
            )
            self.fields["contr_pais_nacionalidade_codi"].required = False

        if "contr_pais_nacionalidade_desc" in self.fields:
            self.fields["contr_pais_nacionalidade_desc"].widget = forms.HiddenInput()
            self.fields["contr_pais_nacionalidade_desc"].required = False

        for f_esocial in ("contr_esocial_qualif_status", "contr_esocial_qualif_mensagem",
                           "contr_esocial_qualif_data_hora", "contr_esocial_integrado",
                           "contr_esocial_integra_data_hora", "contr_esocial_integra_numero_recibo"):
            if f_esocial in self.fields:
                self.fields[f_esocial].required = False
                if f_esocial != "contr_esocial_integrado":
                    try:
                        self.fields[f_esocial].widget.attrs["readonly"] = "readonly"
                        self.fields[f_esocial].widget.attrs["class"] = "form-control contribuinte-readonly"
                    except Exception:
                        pass

    def clean_contr_cpf(self):
        valor = (self.cleaned_data.get("contr_cpf") or "").strip()
        digits = _only_digits(valor)[:11]
        if digits and not _cpf_valido(digits):
            raise forms.ValidationError("Informe um CPF válido.")
        return digits or None

    def clean_contr_nis(self):
        valor = (self.cleaned_data.get("contr_nis") or "").strip()
        return _only_digits(valor)[:11] or None

    def clean_contr_rg(self):
        valor = (self.cleaned_data.get("contr_rg") or "").strip()
        return _only_digits(valor)[:20] or None

    def clean_contr_cep(self):
        valor = (self.cleaned_data.get("contr_cep") or "").strip()
        digits = _only_digits(valor)[:8]
        if digits and len(digits) != 8:
            raise forms.ValidationError("Informe um CEP válido com 8 dígitos.")
        return digits or None

    def clean_contr_ddd(self):
        return _only_digits(self.cleaned_data.get("contr_ddd"))[:2] or None

    def clean_contr_telefone(self):
        return _only_digits(self.cleaned_data.get("contr_telefone"))[:9] or None

    def clean_contr_ddd_celular(self):
        return _only_digits(self.cleaned_data.get("contr_ddd_celular"))[:2] or None

    def clean_contr_celular(self):
        return _only_digits(self.cleaned_data.get("contr_celular"))[:11] or None

    def clean_contr_carteira_trabalho(self):
        return _only_digits(self.cleaned_data.get("contr_carteira_trabalho"))[:7] or None

    def clean_contr_serie_carteira_trabalho(self):
        return _only_digits(self.cleaned_data.get("contr_serie_carteira_trabalho"))[:4] or None

    def clean_contr_digito_serie_carteira_trabalho(self):
        return _only_digits(self.cleaned_data.get("contr_digito_serie_carteira_trabalho"))[:2] or None

    def clean_contr_cnh(self):
        return _only_digits(self.cleaned_data.get("contr_cnh"))[:11] or None

    def clean_contr_categoria_cnh(self):
        valor = (self.cleaned_data.get("contr_categoria_cnh") or "").strip().upper()
        return valor[:5] or None

    def clean_contr_titulo_eleitor(self):
        return _only_digits(self.cleaned_data.get("contr_titulo_eleitor"))[:12] or None

    def clean_contr_zona_titulo(self):
        return _only_digits(self.cleaned_data.get("contr_zona_titulo"))[:4] or None

    def clean_contr_secao_titulo(self):
        return _only_digits(self.cleaned_data.get("contr_secao_titulo"))[:4] or None

    def clean_contr_certificado_reservista(self):
        return _only_digits(self.cleaned_data.get("contr_certificado_reservista"))[:30] or None

    def clean_contr_rne(self):
        return _only_digits(self.cleaned_data.get("contr_rne"))[:20] or None

    def clean_contr_cbo(self):
        return _only_digits(self.cleaned_data.get("contr_cbo"))[:6] or None

    def clean_contr_categoria_esocial(self):
        valor = self.cleaned_data.get("contr_categoria_esocial")
        if valor in (None, ""):
            if "contr_categoria_esocial_desc" in self.cleaned_data:
                self.cleaned_data["contr_categoria_esocial_desc"] = None
            return None
        try:
            valor_int = int(valor)
        except (TypeError, ValueError):
            raise forms.ValidationError("Selecione uma categoria eSocial válida.")
        desc_label = ""
        for cod, desc in CATEGORIA_ESOCIAL_CHOICES:
            if cod in (None, ""):
                continue
            try:
                if int(cod) == valor_int:
                    desc_label = str(desc)
                    break
            except (TypeError, ValueError):
                continue
        if not desc_label:
            desc_label = f"{valor_int} - Categoria {valor_int}"
        self.cleaned_data["contr_categoria_esocial_desc"] = desc_label
        return valor_int

    def clean_contr_cnpj_cpf_origem(self):
        valor = (self.cleaned_data.get("contr_cnpj_cpf_origem") or "").strip()
        digits = _only_digits(valor)
        if digits:
            tipo = self.cleaned_data.get("contr_tipo_cnpj_cpf_origem")
            max_len = 14 if str(tipo or "") == "1" else 11
            digits = digits[:max_len]
        return digits or None

    def clean_contr_pais_nascimento_codi(self):
        valor = self.cleaned_data.get("contr_pais_nascimento_codi")
        if valor in (None, ""):
            return None
        valor_str = str(valor).strip()
        match_codigo = None
        apenas_digitos = "".join(ch for ch in valor_str if ch.isdigit())
        if apenas_digitos:
            try:
                match_codigo = int(apenas_digitos)
            except (TypeError, ValueError):
                match_codigo = None
        if match_codigo is not None and match_codigo in PAISES_POR_CODIGO:
            label = PAISES_POR_CODIGO[match_codigo]
            nome = label.split(" - ", 1)[1] if " - " in label else str(label)
            self.cleaned_data["contr_pais_nascimento_desc"] = nome
            return match_codigo
        if match_codigo is not None and 1 <= match_codigo <= 999:
            self.cleaned_data["contr_pais_nascimento_desc"] = str(match_codigo)
            return match_codigo
        texto_busca = valor_str.lower()
        if texto_busca:
            for cod_num, label in PAISES_POR_CODIGO.items():
                if texto_busca in label.lower():
                    nome = label.split(" - ", 1)[1] if " - " in label else str(label)
                    self.cleaned_data["contr_pais_nascimento_desc"] = nome
                    return cod_num
        raise forms.ValidationError(
            "País não encontrado. Digite o código de 3 dígitos "
            "ou comece a digitar o nome e selecione uma opção da lista."
        )

    def clean_contr_cidade_nascimento_codi(self):
        valor = self.cleaned_data.get("contr_cidade_nascimento_codi")
        if valor in (None, ""):
            return None
        valor_str = str(valor).strip()
        match_codigo = None
        apenas_digitos = "".join(ch for ch in valor_str if ch.isdigit())
        if len(apenas_digitos) >= 2:
            try:
                match_codigo = int(apenas_digitos)
            except (TypeError, ValueError):
                match_codigo = None
        if match_codigo is not None and match_codigo in CIDADES_POR_CODIGO:
            nome, uf = CIDADES_POR_CODIGO[match_codigo]
            self.cleaned_data["contr_cidade_nascimento_desc"] = f"{nome} / {uf}"
            return match_codigo
        if match_codigo is not None and 1 <= len(apenas_digitos) <= 7:
            self.cleaned_data["contr_cidade_nascimento_desc"] = str(match_codigo)
            return match_codigo
        texto_busca = valor_str.lower()
        if texto_busca:
            for cod_num, (n, u) in CIDADES_POR_CODIGO.items():
                l1 = f"{cod_num:07d} — {n} / {u}".lower()
                l2 = f"{n} {u}".lower()
                l3 = f"{n}/{u}".lower()
                if (texto_busca in l1) or (texto_busca in l2) or (texto_busca in l3):
                    self.cleaned_data["contr_cidade_nascimento_desc"] = f"{n} / {u}"
                    return cod_num
        raise forms.ValidationError(
            "Cidade não encontrada. Digite o código IBGE de 7 dígitos "
            "ou comece a digitar o nome/UF e selecione uma opção da lista."
        )

    def clean(self):
        cleaned_data = super().clean()

        def _apenas_digitos(v):
            if v in (None, "", []):
                return ""
            s = str(v).strip()
            return "".join(ch for ch in s if ch.isdigit())

        def _max_digitos(s, max_len):
            d = _apenas_digitos(s)
            return d[:max_len] if d and max_len and len(d) > max_len else d

        TRIM_DIGIT_FIELDS = [
            ("contr_cpf", 11),
            ("contr_nis", 11),
            ("contr_rg", 20),
            ("contr_cep", 8),
            ("contr_ddd", 2),
            ("contr_ddd_celular", 2),
            ("contr_telefone", 9),
            ("contr_celular", 11),
            ("contr_carteira_trabalho", 7),
            ("contr_serie_carteira_trabalho", 4),
            ("contr_digito_serie_carteira_trabalho", 2),
            ("contr_cnh", 11),
            ("contr_titulo_eleitor", 12),
            ("contr_zona_titulo", 4),
            ("contr_secao_titulo", 4),
            ("contr_certificado_reservista", 30),
            ("contr_rne", 20),
            ("contr_cbo", 6),
            ("contr_cnpj_cpf_origem", 14),
        ]
        for campo, max_len in TRIM_DIGIT_FIELDS:
            if campo in cleaned_data:
                val = _max_digitos(cleaned_data.get(campo), max_len)
                cleaned_data[campo] = val or None

        def _to_int_or_none(v):
            if v in (None, "", []):
                return None
            if isinstance(v, int):
                return v
            s = str(v).strip()
            if not s:
                return None
            if s.lstrip("-").isdigit():
                try:
                    return int(s)
                except (TypeError, ValueError):
                    return None
            return None

        for campo in ("contr_pais_nascimento_codi", "contr_cidade_nascimento_codi"):
            cleaned_data[campo] = _to_int_or_none(cleaned_data.get(campo))

        _cat_esocial_codi = cleaned_data.get("contr_categoria_esocial")
        if _cat_esocial_codi in (None, ""):
            cleaned_data["contr_categoria_esocial_desc"] = None
        else:
            try:
                _cat_int = int(_cat_esocial_codi)
            except (TypeError, ValueError):
                _cat_int = None
            _cat_desc = ""
            if _cat_int is not None:
                for cod, desc in CATEGORIA_ESOCIAL_CHOICES:
                    if cod in (None, ""):
                        continue
                    try:
                        if int(cod) == _cat_int:
                            _cat_desc = str(desc)
                            break
                    except (TypeError, ValueError):
                        continue
            if not _cat_desc and _cat_int is not None:
                _cat_desc = f"{_cat_int} - Categoria {_cat_int}"
            cleaned_data["contr_categoria_esocial_desc"] = _cat_desc

        _vinc_codi = cleaned_data.get("contr_vinculo_empregaticio")
        if _vinc_codi in (None, ""):
            cleaned_data["contr_vinculo_empregaticio_desc"] = None
        else:
            try:
                _vinc_int = int(_vinc_codi)
            except (TypeError, ValueError):
                _vinc_int = None
            _vinc_desc = ""
            if _vinc_int is not None:
                for cod, desc in TIPO_VINCULO_EMPREGATICIO_CHOICES:
                    if cod in (None, ""):
                        continue
                    try:
                        if int(cod) == _vinc_int:
                            _vinc_desc = str(desc)
                            break
                    except (TypeError, ValueError):
                        continue
            if not _vinc_desc and _vinc_int is not None:
                _vinc_desc = f"{_vinc_int} - Vínculo {_vinc_int}"
            if _vinc_desc:
                _vinc_desc = _vinc_desc[:120]
            cleaned_data["contr_vinculo_empregaticio_desc"] = _vinc_desc

        for codigo_campo, desc_campo, prefixo, max_len in (
            ("contr_depto", "contr_depto_desc", "Departamento", 80),
            ("contr_ccusto", "contr_ccusto_desc", "Centro de custo", 80),
            ("contr_cargo", "contr_cargo_desc", "Cargo", 80),
            ("contr_cbo", "contr_cbo_desc", "CBO", 160),
        ):
            _cod = cleaned_data.get(codigo_campo)
            if _cod in (None, "", [], ()):
                cleaned_data[desc_campo] = None
                continue
            _cod_str = str(_cod).strip()
            if not _cod_str:
                cleaned_data[desc_campo] = None
                continue
            _desc = f"{_cod_str} - {prefixo} {_cod_str}"
            if max_len and len(_desc) > max_len:
                _desc = _desc[:max_len]
            cleaned_data[desc_campo] = _desc

        _banco_codi = cleaned_data.get("contr_banco")
        if _banco_codi in (None, "", [], ()):
            cleaned_data["contr_banco_desc"] = None
        else:
            _banco_str = str(_banco_codi).strip()
            if not _banco_str:
                cleaned_data["contr_banco_desc"] = None
            else:
                _banco_desc = ""
                for cod, desc in BANCOS_CHOICES:
                    if cod in (None, ""):
                        continue
                    if str(cod).strip() == _banco_str:
                        _banco_desc = str(desc)
                        break
                if not _banco_desc:
                    _banco_desc = f"{_banco_str} - Banco {_banco_str}"
                if len(_banco_desc) > 120:
                    _banco_desc = _banco_desc[:120]
                cleaned_data["contr_banco_desc"] = _banco_desc

        return cleaned_data
