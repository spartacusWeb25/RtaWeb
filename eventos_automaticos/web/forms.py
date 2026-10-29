import json

from django import forms

from eventos_automaticos.services.logic import (
    EventosAutomaticosService,
    TIPO_CALCULO_DEFAULT,
    TIPO_CALCULO_LABELS,
    _safe_int,
)


class EventoAutomaticoAdicionarForm(forms.Form):
    even_tipo_calculo = forms.CharField(widget=forms.HiddenInput())
    even_codi = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )
    even_codi_search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm js-evento-search-input",
                "autocomplete": "off",
                "placeholder": "Digite código ou descrição do evento",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        self.db_alias = kwargs.pop("db_alias", None)
        self.banco = kwargs.pop("banco", None)
        self.empr_fixo = kwargs.pop("empr_fixo", 1)
        self.tipo_calculo = str(kwargs.pop("tipo_calculo", TIPO_CALCULO_DEFAULT) or TIPO_CALCULO_DEFAULT)
        super().__init__(*args, **kwargs)

        self.fields["even_tipo_calculo"].initial = self.tipo_calculo
        self.event_choices = EventosAutomaticosService.listar_eventos_choices(
            banco=self.banco,
            db_alias=self.db_alias,
            codigo_empresa=self.empr_fixo,
        )
        self.event_search_options = [
            {
                "code": int(valor),
                "label": str(label),
                "desc": str(label).split(" - ", 1)[1] if " - " in str(label) else str(label),
            }
            for valor, label in self.event_choices
            if str(valor or "").strip()
        ]
        self.event_search_options_json = json.dumps(self.event_search_options, ensure_ascii=True)

        valor_atual = None
        texto_atual = ""
        if self.is_bound:
            valor_atual = self.data.get("even_codi")
            texto_atual = str(self.data.get("even_codi_search") or "").strip()
        else:
            valor_atual = self.initial.get("even_codi")
            texto_atual = str(self.initial.get("even_codi_search") or "").strip()

        codigo_atual = _safe_int(valor_atual)
        if codigo_atual is not None and not texto_atual:
            texto_atual = self._get_label_by_codigo(codigo_atual)
        self.fields["even_codi"].initial = codigo_atual
        self.fields["even_codi_search"].initial = texto_atual

    def clean_even_tipo_calculo(self):
        tipo = str(self.cleaned_data.get("even_tipo_calculo") or "").strip()
        if tipo not in TIPO_CALCULO_LABELS:
            raise forms.ValidationError("A aba informada é inválida.")
        return tipo

    def _get_label_by_codigo(self, codigo):
        codigo_int = _safe_int(codigo)
        if codigo_int is None:
            return ""
        for item in self.event_search_options:
            if item["code"] == codigo_int:
                return item["label"]
        return str(codigo_int)

    def _resolver_codigo_por_texto(self, texto):
        texto_limpo = str(texto or "").strip()
        if not texto_limpo:
            return None

        texto_lower = texto_limpo.lower()
        matches_label = [item for item in self.event_search_options if item["label"].lower() == texto_lower]
        if matches_label:
            return matches_label[0]["code"]

        codigo_digitos = _safe_int(texto_limpo)
        if codigo_digitos is not None:
            for item in self.event_search_options:
                if item["code"] == codigo_digitos:
                    return codigo_digitos

        matches_desc = [item for item in self.event_search_options if texto_lower in item["desc"].lower()]
        if len(matches_desc) == 1:
            return matches_desc[0]["code"]
        return None

    def clean(self):
        cleaned = super().clean()
        codigo = _safe_int(cleaned.get("even_codi"))
        texto = str(cleaned.get("even_codi_search") or "").strip()

        if codigo is None:
            codigo = self._resolver_codigo_por_texto(texto)

        if codigo is None:
            self.add_error("even_codi_search", "Selecione um evento válido.")
            return cleaned

        cleaned["even_codi"] = codigo
        cleaned["even_codi_search"] = self._get_label_by_codigo(codigo)
        return cleaned
