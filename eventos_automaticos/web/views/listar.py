from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from eventos_automaticos.mixin import EventosAutomaticosMixin
from eventos_automaticos.services.logic import (
    EventosAutomaticosService,
    TIPO_CALCULO_CHOICES,
)
from eventos_automaticos.web.forms import EventoAutomaticoAdicionarForm


class EventosAutomaticosListView(EventosAutomaticosMixin, TemplateView):
    template_name = "eventos_automaticos/listar.html"

    def _resolve_target_tab(self, raw_tipo):
        tipo = str(raw_tipo or "").strip()
        for codigo, _ in TIPO_CALCULO_CHOICES:
            if codigo == tipo:
                return codigo
        return self.aba_ativa

    def _build_tab_forms(self, data=None):
        forms = {}
        for tipo, _ in TIPO_CALCULO_CHOICES:
            forms[tipo] = EventoAutomaticoAdicionarForm(
                data=data if data is not None and str(data.get("even_tipo_calculo") or "") == tipo else None,
                db_alias=self.db_alias,
                banco=self.banco_limpo,
                empr_fixo=self.EMPRESA_FIXA_CODIGO,
                tipo_calculo=tipo,
            )
        return forms

    def _get_url_listar(self, aba=None):
        aba_param = aba or self.aba_ativa
        return reverse("eventos_automaticos:listar") + f"?banco={self.request.banco or 'rta0001'}&aba={aba_param}"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Eventos automáticos"
        ctx["aba_ativa"] = self.aba_ativa
        ctx["empresa_nome"] = self.obter_nome_empresa_contexto()
        ctx["filial_nome"] = self.obter_nome_filial_contexto()
        ctx["empr_padrao_cod"] = self.EMPRESA_FIXA_CODIGO
        ctx["fili_padrao_cod"] = self.FILIAL_FIXA_CODIGO
        eventos_por_tipo = EventosAutomaticosService.listar_por_tipo(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=self.EMPRESA_FIXA_CODIGO,
            codigo_filial=self.FILIAL_FIXA_CODIGO,
        )
        forms_por_tipo = kwargs.get("forms_por_tipo") or self._build_tab_forms()
        ctx["abas"] = [
            {
                "codigo": codigo,
                "titulo": titulo,
                "form": forms_por_tipo[codigo],
                "eventos": eventos_por_tipo.get(codigo, []),
            }
            for codigo, titulo in TIPO_CALCULO_CHOICES
        ]
        return ctx

    def post(self, request, *args, **kwargs):
        acao = str(request.POST.get("acao") or "").strip().lower()
        if acao == "adicionar":
            return self._post_adicionar()
        if acao == "excluir":
            return self._post_excluir()
        messages.warning(request, "Ação inválida para eventos automáticos.")
        return redirect(self._get_url_listar())

    def _post_adicionar(self):
        form = EventoAutomaticoAdicionarForm(
            data=self.request.POST,
            db_alias=self.db_alias,
            banco=self.banco_limpo,
            empr_fixo=self.EMPRESA_FIXA_CODIGO,
            tipo_calculo=self.request.POST.get("even_tipo_calculo"),
        )
        target_tab = self._resolve_target_tab(self.request.POST.get("even_tipo_calculo"))
        if not form.is_valid():
            forms_por_tipo = self._build_tab_forms(self.request.POST)
            forms_por_tipo[target_tab] = form
            context = self.get_context_data(forms_por_tipo=forms_por_tipo)
            return self.render_to_response(context)

        try:
            EventosAutomaticosService.adicionar_evento(
                banco=self.banco_limpo,
                db_alias=self.db_alias,
                codigo_empresa=self.EMPRESA_FIXA_CODIGO,
                codigo_filial=self.FILIAL_FIXA_CODIGO,
                even_tipo_calculo=form.cleaned_data["even_tipo_calculo"],
                even_codi=form.cleaned_data["even_codi"],
            )
        except ValidationError as exc:
            form.add_error(None, str(exc))
            forms_por_tipo = self._build_tab_forms(self.request.POST)
            forms_por_tipo[target_tab] = form
            context = self.get_context_data(forms_por_tipo=forms_por_tipo)
            return self.render_to_response(context)
        except Exception as exc:
            form.add_error(None, str(exc))
            forms_por_tipo = self._build_tab_forms(self.request.POST)
            forms_por_tipo[target_tab] = form
            context = self.get_context_data(forms_por_tipo=forms_por_tipo)
            return self.render_to_response(context)

        messages.success(self.request, "Evento automático adicionado com sucesso.")
        return redirect(self._get_url_listar(form.cleaned_data["even_tipo_calculo"]))

    def _post_excluir(self):
        tipo = self.request.POST.get("even_tipo_calculo")
        codigo = self.request.POST.get("even_codi")
        try:
            EventosAutomaticosService.excluir_evento(
                banco=self.banco_limpo,
                db_alias=self.db_alias,
                codigo_empresa=self.EMPRESA_FIXA_CODIGO,
                codigo_filial=self.FILIAL_FIXA_CODIGO,
                even_tipo_calculo=tipo,
                even_codi=codigo,
            )
        except ValidationError as exc:
            messages.error(self.request, str(exc))
            return redirect(self._get_url_listar(tipo))
        except Exception as exc:
            messages.error(self.request, str(exc))
            return redirect(self._get_url_listar(tipo))

        messages.success(self.request, "Evento automático excluído com sucesso.")
        return redirect(self._get_url_listar(tipo))
