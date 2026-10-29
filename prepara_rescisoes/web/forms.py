from django import forms
from datetime import date

from prepara_rescisoes.models import PreparaRescisoes


# ==============================================================================
# CHOICES DAS COMBOBOXES (Destacadas no print, o usuario pode add mais depois!)
# 1a opcao SEMPRE = "Selecione"  (valor vazio -> obrigatorio selecionar se quiser)
# ==============================================================================
CHOICES_INICIATIVA = [
    ("", "Selecione"),
    (1,  "Empresa"),
    (2,  "Empregado"),
    (3,  "Pedido mútuo acordo"),
    (4,  "Justa causa"),
    (5,  "Sem justa causa"),
    (6,  "Falecimento"),
]

CHOICES_AVISO_PREVIO = [
    ("", "Selecione"),
    (1,  "Indenizado"),
    (2,  "Trabalhado"),
    (3,  "Sem Aviso"),
    (4,  "S/Data"),
    (5,  "Dispensado sem justa causa"),
    (6,  "Dispensado com justa causa"),
]

CHOICES_GFD = [
    ("", "Selecione"),
    (1,  "Guia FGTS Digital (Mensal) / Exporta GFIP"),
    (2,  "Conforme tipo de afastamento do colaborador"),
    (3,  "Não informar em GFD (Somente GPS SEFIP)"),
]

CHOICES_SAQUE_CODI = [
    ("", "Selecione"),
    ("01", "01 - Demissão sem justa causa pelo empregador, inclusive rescisão indireta"),
    ("02", "02 - Rescisão por culpa recíproca ou força maior reconhecida pela Justiça"),
    ("03", "03 - Extinção da empresa, falência ou outras hipóteses específicas previstas nas regras do FGTS"),
    ("04", "04 - Término de contrato por prazo determinado, inclusive contrato de experiência"),
    ("07", "07 - Rescisão por acordo entre empregado e empregador"),

]

CHOICES_FGTS_MOTIVOS = [
    ("", "Selecione"),
    ("H", "H - Rescisão com justa causa, por iniciativa do empregador"),
    ("I1", "I1 - Rescisão sem justa causa, por iniciativa do empregador"),
    ("I2", "I2 - Rescisão por culpa recíproca ou força maior"),
    ("I3", "I3 - Rescisão por finalização de contrato a termo"),
    ("I4", "I4 - Rescisão sem justa causa do contrato do empregado doméstico"),
    ("I5", "I5 - Rescisão do contrato por motivo de acordo"),
    ("J", "J - Outros motivos de rescisão de contrato de trabalho"),
    ("S2", "S2 - Falecimento"),
    ("S3", "S3 - Falecimento motivado por acidente de trabalho"),
    ("U1", "U1 - Aposentadoria sem continuidade do vínculo empregatício"),
    ("N1", "N1 - Transferência de empregado para outro estabelecimento da empresa"),
    ("N2", "N2 - Transferência de empregado para outra empresa que assuma os encargos"),
]

CHOICES_CAGED_MOTIVOS = [
    ("", "Selecione"),
    ("31", "31 - Dispensa sem justa causa"),
    ("32", "32 - Dispensa por justa causa"),
    ("40", "40 - Desligamento por iniciativa própria (pedido)"),
    ("45", "45 - Término de contrato"),
    ("50", "50 - Desligamento por aposentadoria"),
    ("60", "60 - Desligamento por morte"),
    ("80", "80 - Transferência de saída"),
    ("90", "90 - Desligamento por acordo entre empregado e empregador"),
]

CHOICES_RAIS_MOTIVOS = [
    ("", "Selecione"),
    ("10", "10 - Rescisão com justa causa por iniciativa do empregador."),
    ("11", "11 - Rescisão sem justa causa por iniciativa do empregador."),
    ("12", "12 - Término do contrato de trabalho."),
    ("20", "20 - Rescisão com justa causa por iniciativa do empregado (rescisão indireta)."),
    ("21", "21 - Rescisão sem justa causa por iniciativa do empregado."),
    ("22", "22 - Posse em outro cargo inacumulável (específico para servidor público)."),
    ("30", "30 - Transferência/mov. com ônus para o cedente."),
    ("31", "31 - Transferência/mov. sem ônus para o cedente."),
    ("32", "32 - Readaptação (servidor público)."),
    ("33", "33 - Cessão."),
    ("34", "34 - Redistribuição (servidor público)."),
    ("40", "40 - Mudança de regime trabalhista."),
    ("50", "50 - Reforma de militar para a reserva remunerada."),
    ("60", "60 - Falecimento."),
    ("62", "62 - Falecimento decorrente de acidente do trabalho típico."),
    ("63", "63 - Falecimento decorrente de acidente de trabalho de trajeto."),
    ("64", "64 - Falecimento decorrente de doença profissional."),
    ("70", "70 - Aposentadoria por tempo de serviço, com rescisão contratual."),
    ("71", "71 - Aposentadoria por tempo de serviço, sem rescisão contratual."),
    ("72", "72 - Aposentadoria por idade, com rescisão contratual."),
    ("73", "73 - Aposentadoria por invalidez, decorrente de acidente de trabalho."),
    ("74", "74 - Aposentadoria por invalidez, decorrente de doença profissional."),
    ("75", "75 - Aposentadoria compulsória."),
    ("76", "76 - Aposentadoria por invalidez, exceto a decorrente de doença profissional ou acidente de trabalho."),
    ("78", "78 - Aposentadoria por idade, sem rescisão contratual."),
    ("79", "79 - Aposentadoria especial."),
    ("80", "80 - Rescisão determinada pela justiça."),
    ("90", "90 - Desligamento por Acordo entre empregado e empregador. art. 484-A, Lei 13.467/17."),
]

CHOICES_HOMOLOGNET_MOTIVOS = [
    ("", "Selecione"),
    ("SJ2", "SJ2 - Despedida sem justa causa, pelo empregador"),
    ("JC2", "JC2 - Dispensa por justa causa, pelo empregador"),
    ("RA2", "RA2 - Rescisão antecipada, pelo empregador, de contrato por prazo determinado"),
    ("FE2", "FE2 - Rescisão por falecimento do empregador individual sem continuidade da atividade"),
    ("FE1", "FE1 - Rescisão por falecimento do empregador individual por opção do empregado"),
    ("RA1", "RA1 - Rescisão antecipada, pelo empregado, do contrato por prazo determinado"),
    ("SJ1", "SJ1 - Rescisão a pedido do empregado"),
    ("FT1", "FT1 - Rescisão do contrato por falecimento do empregado"),
    ("PD0", "PD0 - Extinção normal do contrato por prazo determinado"),
    ("RI2", "RI2 - Rescisão indireta"),
    ("CR0", "CR0 - Rescisão por culpa recíproca"),
    ("FM0", "FM0 - Rescisão por força maior"),
    ("NC0", "NC0 - Rescisão por nulidade do contrato de trabalho, declarada em decisão judicial"),
    ("Não Definido M.T.E.", "Não Definido M.T.E. - Rescisão de contrato de trabalho por acordo entre trabalhador e empregador"),
]

CHOICES_MOTIVO_ESOCIAL = [
    ("", "Selecione"),
    ("01", "01 - Rescisão com justa causa, por iniciativa do empregador"),
    ("02", "02 - Rescisão sem justa causa, por iniciativa do empregador"),
    ("03", "03 - Rescisão antecipada do contrato a termo por iniciativa do empregador"),
    ("04", "04 - Rescisão antecipada do contrato a termo por iniciativa do empregado"),
    ("05", "05 - Rescisão por culpa recíproca"),
    ("06", "06 - Rescisão por término do contrato a termo"),
    ("07", "07 - Rescisão do contrato de trabalho por iniciativa do empregado"),
    ("08", "08 - Rescisão do contrato de trabalho por interesse do(a) empregado(a), nas hipóteses previstas nos arts. 394 e 483, § 1º da CLT"),
    ("09", "09 - Rescisão por opção do empregado em virtude de falecimento do empregador individual ou empregador doméstico"),
    ("10", "10 - Rescisão por falecimento do empregado"),
    ("11", "11 - Transferência de empregado para empresa do mesmo grupo empresarial que tenha assumido os encargos trabalhistas, sem que tenha havido rescisão do contrato de trabalho"),
    ("12", "12 - Transferência de empregado de empresa consorciada para o consórcio que tenha assumido os encargos trabalhistas, e vice-versa, sem que tenha havido rescisão do contrato de trabalho"),
    ("13", "13 - Transferência de empregado de empresa ou consórcio, para outra empresa ou consórcio que tenha assumido os encargos trabalhistas por motivo de sucessão (fusão, cisão ou incorporação), sem que tenha havido rescisão do contrato de trabalho"),
    ("14", "14 - Rescisão do contrato de trabalho por encerramento da empresa, de seus estabelecimentos ou supressão de parte de suas atividades ou falecimento do empregador individual ou empregador doméstico sem continuação da atividade"),
    ("15", "15 - Rescisão do contrato de aprendizagem por desempenho insuficiente, inadaptação ou ausência injustificada à escola que implique perda do ano letivo"),
    ("16", "16 - Declaração de nulidade do contrato de trabalho por infringência ao inciso II do art. 37 da Constituição Federal, quando mantido o direito ao salário"),
    ("17", "17 - Rescisão Indireta do Contrato de Trabalho"),
    ("18", "18 - Aposentadoria Compulsória (somente para categorias de trabalhadores 301 a 309)"),
    ("19", "19 - Aposentadoria por idade (somente para categorias de trabalhadores 301 a 309)"),
    ("20", "20 - Aposentadoria por idade e tempo de contribuição (somente categorias 301 a 309)"),
    ("21", "21 - Reforma Militar (somente para categorias de trabalhadores 301 a 309)"),
    ("22", "22 - Reserva Militar (somente para categorias de trabalhadores 301 a 309)"),
    ("23", "23 - Exoneração (somente para categorias de trabalhadores 301 a 309)"),
    ("24", "24 - Demissão (somente para categorias de trabalhadores 301 a 309)"),
    ("25", "25 - Vacância para assumir outro cargo efetivo (somente para categorias de trabalhadores 301 a 309)"),
    ("26", "26 - Rescisão do contrato de trabalho por paralisação temporária ou definitiva da empresa, estabelecimento ou parte das atividades motivada por atos de autoridade municipal, estadual ou federal"),
    ("27", "27 - Rescisão por motivo de força maior"),
    ("28", "28 - Término da Cessão/Requisição"),
    ("29", "29 - Redistribuição"),
    ("30", "30 - Mudança de Regime Trabalhista"),
    ("31", "31 - Reversão de Reintegração"),
    ("32", "32 - Extravio de Militar"),
    ("33", "33 - Rescisão por acordo entre as partes (art. 484-A da CLT)"),
    ("34", "34 - Transferência de titularidade do empregador doméstico para outro representante da mesma unidade familiar"),
    ("35", "35 - Extinção do contrato de trabalho intermitente"),
    ("36", "36 - Mudança de CPF"),
]

EMPTY_SELECT_CHOICE = [("", "Selecione")]

# Dicts auxiliares para AUTO-PREENCHIMENTO do campo _desc correspondente
# (a combobox grava o CODIGO no _codi; o texto no _desc)
_MAP_INICIATIVA_DESC = {str(cod): desc for (cod, desc) in CHOICES_INICIATIVA if cod != ""}
_MAP_AVISO_PREVIO_DESC = {str(cod): desc for (cod, desc) in CHOICES_AVISO_PREVIO if cod != ""}
_MAP_GFD_DESC = {str(cod): desc for (cod, desc) in CHOICES_GFD if cod != ""}
_MAP_SAQUE_CODI = {str(cod): desc for (cod, desc) in CHOICES_SAQUE_CODI if cod != ""}


FIELD_LABELS = {
    "prep_codi": "Código",
    "prep_desc": "Descrição (título)",
    "prep_descricao": "Descrição",
    "prep_inativo": "Inativo",

    # --- Dados Gerais ---
    "prep_iniciativa_codi": "Iniciativa",
    "prep_iniciativa_desc": "Iniciativa (descrição)",
    "prep_aviso_previo_codi": "Aviso prévio",
    "prep_aviso_previo_desc": "Aviso prévio (descrição)",
    "prep_inden_ferias_13": "Indenização 1/12 de férias e 13º",

    "prep_saque_codi": "Código saque",
    "prep_saque_desc": "Código saque (descrição)",

    "prep_fgts_codi": "FGTS",
    "prep_fgts_desc": "FGTS (descrição)",
    "prep_fgts_int_codi": "FGTS intermitente",
    "prep_fgts_int_desc": "FGTS intermitente (descrição)",

    "prep_caged_codi": "CAGED",
    "prep_caged_desc": "CAGED (descrição)",
    "prep_rais_codi": "RAIS",
    "prep_rais_desc": "RAIS (descrição)",

    "prep_gfd_codi": "GFD / GRRF",
    "prep_gfd_desc": "GFD / GRRF (descrição)",
    "prep_homolognet_codi": "Código HomologNet",
    "prep_homolognet_desc": "HomologNet (descrição)",
    "prep_motivo_esocial_codi": "Motivo eSocial",
    "prep_motivo_esocial_desc": "Motivo eSocial (descrição)",

    # --- Checkboxes ---
    "prep_justa_causa": "Justa causa",
    "prep_inden_contr_exp": "Indenização contrato experiência",
    "prep_emitir_seg_desemp": "Emitir seguro desemprego",
    "prep_50_aviso_inden": "50% do aviso indenizado",
    "prep_estabilidade": "Estabilidade",
    "prep_nao_calc_multa_resc": "Não calcula multa rescisória",
    "prep_50_verbas_inden": "50% das verbas indenizadas (aviso/férias/13º)",
    "prep_rescisao_fixa": "Rescisão fixa",

    "prep_usuario_inc": "Usuário inclusão",
    "prep_data_inc": "Data inclusão",
    "prep_usuario_alt": "Usuário alteração",
    "prep_data_alt": "Data alteração",
}

_DIGITS_ONLY_FIELDS = (
    "prep_codi",
)


def _safe_int(value):
    try:
        if value is None:
            return None
        s = str(value).strip()
        if not s or not s.isdigit():
            return None
        return int(s)
    except Exception:
        return None


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _choice_value(value):
    return str(value or "").strip()


def _choices_desc_map(choices):
    return {
        _choice_value(cod): str(desc or "").strip()
        for cod, desc in choices
        if _choice_value(cod)
    }


def _append_choice_if_missing(choices, code, desc):
    code_norm = _choice_value(code)
    if not code_norm:
        return choices
    if any(_choice_value(existing_code) == code_norm for existing_code, _ in choices):
        return choices
    label = str(desc or "").strip() or code_norm
    return list(choices) + [(code_norm, label)]


class PreparaRescisoesForm(forms.ModelForm):

    DYNAMIC_COMBO_FIELDS = (
    )

    class Meta:
        model = PreparaRescisoes
        fields = "__all__"
        labels = FIELD_LABELS
        widgets = {
            "registro": forms.HiddenInput(),
            "prep_empr": forms.HiddenInput(),
            "prep_fili": forms.HiddenInput(),
            "prep_codi": forms.HiddenInput(),

            # prep_desc: REMOVIDO da tela (mantém no banco). O valor é
            # preenchido AUTOMATICAMENTE no clean() com o conteúdo de
            # prep_descricao (Descrição principal) para manter compatibilidade.
            "prep_desc": forms.HiddenInput(),

            "prep_descricao": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Ex.: Demissão Sem Justa Causa",
                    "maxlength": 200,
                }
            ),

            # prep_inativo: REMOVIDO da tela (mantém no banco). Valor padrão
            # False. Se um dia precisar inativar, pode ser feito pelo service
            # ou via SQL direto no banco.
            "prep_inativo": forms.HiddenInput(),

            # --- Iniciativa + Aviso Prévio (COMBOBOXES: Select 1 unico campo) ---
            #     Codigo grava no _codi integer, o texto (descricao) é auto
            #     preenchido via clean() + hidden input _desc.
            "prep_iniciativa_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_iniciativa_desc"},
                choices=CHOICES_INICIATIVA,
            ),
            "prep_iniciativa_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),
            "prep_aviso_previo_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_aviso_previo_desc"},
                choices=CHOICES_AVISO_PREVIO,
            ),
            "prep_aviso_previo_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),
            "prep_inden_ferias_13": forms.CheckboxInput(attrs={"class": "form-check-input"}),

            # --- Demais opções em combobox ---
            "prep_saque_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_saque_desc"},
                choices=CHOICES_SAQUE_CODI,
            ),
            "prep_saque_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),
            "prep_fgts_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_fgts_desc"},
                choices=EMPTY_SELECT_CHOICE,
            ),
            "prep_fgts_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),
            "prep_fgts_int_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_fgts_int_desc"},
                choices=EMPTY_SELECT_CHOICE,
            ),
            "prep_fgts_int_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),
            "prep_caged_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_caged_desc"},
                choices=EMPTY_SELECT_CHOICE,
            ),
            "prep_caged_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),
            "prep_rais_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_rais_desc"},
                choices=EMPTY_SELECT_CHOICE,
            ),
            "prep_rais_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),

            # --- GFD / HomologNet / Motivo eSocial (todos como combobox; GFD já fixo) ---
            "prep_gfd_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_gfd_desc"},
                choices=CHOICES_GFD,
            ),
            "prep_gfd_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),
            "prep_homolognet_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_homolognet_desc"},
                choices=EMPTY_SELECT_CHOICE,
            ),
            "prep_homolognet_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),
            "prep_motivo_esocial_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_motivo_esocial_desc"},
                choices=EMPTY_SELECT_CHOICE,
            ),
            "prep_motivo_esocial_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),

            # --- Checkboxes (booleans) ---
            "prep_justa_causa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_inden_contr_exp": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_emitir_seg_desemp": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_50_aviso_inden": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_estabilidade": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_nao_calc_multa_resc": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_50_verbas_inden": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_rescisao_fixa": forms.CheckboxInput(attrs={"class": "form-check-input"}),

            # --- LOGS (auditoria) — ocultos, preenchidos automaticamente pelo service ---
            "prep_usuario_inc": forms.HiddenInput(),
            "prep_data_inc": forms.HiddenInput(),
            "prep_usuario_alt": forms.HiddenInput(),
            "prep_data_alt": forms.HiddenInput(),
        }

    def __init__(self, *args, db_alias=None, banco=None, empr_fixo=1, fili_fixo=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_alias = db_alias or "default"
        self.banco = banco
        self.empr_fixo = int(empr_fixo or 1)
        self.fili_fixo = int(fili_fixo or 1)
        self._combo_desc_maps = {
            "prep_iniciativa_codi": _MAP_INICIATIVA_DESC,
            "prep_aviso_previo_codi": _MAP_AVISO_PREVIO_DESC,
            "prep_saque_codi": _MAP_SAQUE_CODI,
            "prep_gfd_codi": _MAP_GFD_DESC,
        }

        for fname in _DIGITS_ONLY_FIELDS:
            if fname in self.fields:
                f = self.fields[fname]
                attrs = dict(f.widget.attrs or {})
                attrs.setdefault("data-digits-only", "true")
                attrs.setdefault("inputmode", "numeric")
                f.widget.attrs = attrs

        # Todos campos opcionais (exceto registro/empr/fili/codi que são Hidden + PK)
        for fname, field in self.fields.items():
            if fname.startswith("prep_") and fname not in ("prep_inativo",):
                field.required = False

        if "prep_inativo" in self.fields:
            self.fields["prep_inativo"].required = False

        self._configure_combo_field("prep_saque_codi", "prep_saque_desc", CHOICES_SAQUE_CODI)
        self._configure_combo_field(
            "prep_fgts_codi",
            "prep_fgts_desc",
            self._load_fixed_choices("prep_fgts_codi", "prep_fgts_desc", CHOICES_FGTS_MOTIVOS),
        )
        self._configure_combo_field(
            "prep_fgts_int_codi",
            "prep_fgts_int_desc",
            self._load_fixed_choices("prep_fgts_int_codi", "prep_fgts_int_desc", CHOICES_FGTS_MOTIVOS),
        )
        self._configure_combo_field(
            "prep_caged_codi",
            "prep_caged_desc",
            self._load_fixed_choices("prep_caged_codi", "prep_caged_desc", CHOICES_CAGED_MOTIVOS),
        )
        self._configure_combo_field(
            "prep_rais_codi",
            "prep_rais_desc",
            self._load_fixed_choices("prep_rais_codi", "prep_rais_desc", CHOICES_RAIS_MOTIVOS),
        )
        self._configure_combo_field(
            "prep_homolognet_codi",
            "prep_homolognet_desc",
            self._load_fixed_choices("prep_homolognet_codi", "prep_homolognet_desc", CHOICES_HOMOLOGNET_MOTIVOS),
        )
        self._configure_combo_field(
            "prep_motivo_esocial_codi",
            "prep_motivo_esocial_desc",
            self._load_fixed_choices("prep_motivo_esocial_codi", "prep_motivo_esocial_desc", CHOICES_MOTIVO_ESOCIAL),
        )
        for code_field, desc_field in self.DYNAMIC_COMBO_FIELDS:
            self._configure_combo_field(
                code_field,
                desc_field,
                self._load_distinct_choices(code_field, desc_field),
            )

    def _load_fixed_choices(self, code_field, desc_field, choices):
        current_code = _choice_value(
            self.data.get(code_field)
            if self.is_bound else getattr(self.instance, code_field, None)
        )
        current_desc = (
            self.data.get(desc_field)
            if self.is_bound else getattr(self.instance, desc_field, None)
        )
        return _append_choice_if_missing(list(choices), current_code, current_desc)

    def _load_distinct_choices(self, code_field, desc_field):
        choices = list(EMPTY_SELECT_CHOICE)
        try:
            rows = (
                PreparaRescisoes.objects.using(self.db_alias)
                .values_list(code_field, desc_field)
            )
            seen = set()
            dynamic_choices = []
            for code, desc in rows:
                code_norm = _choice_value(code)
                if not code_norm:
                    continue
                label = str(desc or "").strip() or code_norm
                key = (code_norm, label)
                if key in seen:
                    continue
                seen.add(key)
                dynamic_choices.append((code_norm, label))
            dynamic_choices.sort(key=lambda item: (item[1].lower(), item[0].lower()))
            choices.extend(dynamic_choices)
        except Exception:
            pass

        current_code = _choice_value(
            self.data.get(code_field)
            if self.is_bound else getattr(self.instance, code_field, None)
        )
        current_desc = (
            self.data.get(desc_field)
            if self.is_bound else getattr(self.instance, desc_field, None)
        )
        return _append_choice_if_missing(choices, current_code, current_desc)

    def _configure_combo_field(self, code_field, desc_field, choices):
        if code_field in self.fields:
            self.fields[code_field].widget.choices = choices
        self._combo_desc_maps[code_field] = _choices_desc_map(choices)

    def clean_prep_codi(self):
        valor = self.cleaned_data.get("prep_codi")
        return _safe_int(valor)

    def clean_prep_iniciativa_codi(self):
        # Combobox Select: valor chega como str "1" / "2" / "" (selecionar = vazio)
        return _safe_int(self.cleaned_data.get("prep_iniciativa_codi"))

    def clean_prep_aviso_previo_codi(self):
        return _safe_int(self.cleaned_data.get("prep_aviso_previo_codi"))

    def clean_prep_gfd_codi(self):
        return _safe_int(self.cleaned_data.get("prep_gfd_codi"))

    def validate_unique(self):
        banco_limpo = _digits_only(self.banco or "")
        empr = self.empr_fixo or _safe_int(self.cleaned_data.get("prep_empr")) or 1
        fili = self.fili_fixo or _safe_int(self.cleaned_data.get("prep_fili")) or 1
        codi = _safe_int(self.cleaned_data.get("prep_codi")) or _safe_int(self.initial.get("prep_codi"))

        if not (banco_limpo and empr and fili and codi):
            return

        from prepara_rescisoes.models import PreparaRescisoes
        qs = PreparaRescisoes.objects.using(self.db_alias).filter(
            registro=banco_limpo,
            prep_empr=int(empr),
            prep_fili=int(fili),
            prep_codi=int(codi),
        )
        instance = getattr(self, "instance", None)
        is_editar = False
        if instance is not None:
            try:
                is_editar = all(getattr(instance, f, None) is not None for f in (
                    "registro", "prep_empr", "prep_fili", "prep_codi"
                ))
            except Exception:
                is_editar = False
        if is_editar:
            try:
                qs = qs.exclude(
                    registro=getattr(instance, "registro"),
                    prep_empr=getattr(instance, "prep_empr"),
                    prep_fili=getattr(instance, "prep_fili"),
                    prep_codi=getattr(instance, "prep_codi"),
                )
            except Exception:
                pass

        try:
            duplicado = qs.exists()
        except Exception:
            # Caso a tabela ainda não exista no Postgres (ainda não rodou o SQL),
            # pula a validação de duplicidade sem crashar.
            duplicado = False

        if duplicado:
            self.add_error(
                "prep_codi",
                f"Já existe uma Preparação de Rescisão com o Código {codi} para a Empresa/Filial selecionada.",
            )

    def clean(self):
        cd = super().clean() or {}
        today = date.today()
        if self.instance is not None:
            # Preenche automaticamente empresa/filial fixa no modo criar
            if not getattr(self.instance, "prep_empr", None):
                self.instance.prep_empr = self.empr_fixo
            if not getattr(self.instance, "prep_fili", None):
                self.instance.prep_fili = self.fili_fixo

        # ==============================================================
        # AUTO-PREENCHIMENTO: descrições das comboboxes a partir do valor
        # selecionado no Select. Grava o texto no campo _desc correspondente.
        # ==============================================================
        _auto = (
            ("prep_iniciativa_codi", "prep_iniciativa_desc"),
            ("prep_aviso_previo_codi", "prep_aviso_previo_desc"),
            ("prep_saque_codi", "prep_saque_desc"),
            ("prep_fgts_codi", "prep_fgts_desc"),
            ("prep_fgts_int_codi", "prep_fgts_int_desc"),
            ("prep_caged_codi", "prep_caged_desc"),
            ("prep_rais_codi", "prep_rais_desc"),
            ("prep_gfd_codi", "prep_gfd_desc"),
            ("prep_homolognet_codi", "prep_homolognet_desc"),
            ("prep_motivo_esocial_codi", "prep_motivo_esocial_desc"),
        )
        for cod_key, desc_key in _auto:
            mapa = getattr(self, "_combo_desc_maps", {}).get(cod_key, {})
            code_value = _choice_value(cd.get(cod_key))
            if code_value:
                desc = mapa.get(code_value, "")
                if desc:
                    cd[desc_key] = desc
                    if self.instance is not None:
                        setattr(self.instance, desc_key, desc)
            elif not cd.get(desc_key):
                cd[desc_key] = ""
                if self.instance is not None:
                    setattr(self.instance, desc_key, "")

        # Preenchimento automático de inicial prep_descricao para prep_desc
        # (se um estiver vazio e o outro não)
        if cd is not None:
            d = cd.get("prep_desc")
            dc = cd.get("prep_descricao")
            if d and not dc:
                cd["prep_descricao"] = str(d).strip()
                if self.instance is not None:
                    self.instance.prep_descricao = str(d).strip()
            elif dc and not d:
                cd["prep_desc"] = str(dc).strip()
                if self.instance is not None:
                    self.instance.prep_desc = str(dc).strip()
            # Garante valores padrão para bools
            for b in ("prep_inativo", "prep_inden_ferias_13",
                      "prep_justa_causa", "prep_inden_contr_exp",
                      "prep_emitir_seg_desemp", "prep_50_aviso_inden",
                      "prep_estabilidade", "prep_nao_calc_multa_resc",
                      "prep_50_verbas_inden", "prep_rescisao_fixa"):
                if b not in cd or cd.get(b) in (None, ""):
                    cd[b] = False
                    if self.instance is not None:
                        setattr(self.instance, b, False)
        return cd
