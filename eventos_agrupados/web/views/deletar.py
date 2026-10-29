from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from eventos_agrupados.services.logic import EventosAgrupadosService, _digits_only


class EventosAgrupadosDeleteView(TemplateView):
    template_name = "eventos_agrupados/confirmar_exclusao.html"
    success_url_name = "eventos_agrupados:listar"
    success_message = "Configuração de eventos agrupados excluída com sucesso."

    EMPRESA_FIXA_CODIGO = 1
    FILIAL_FIXA_CODIGO = 1

    @property
    def banco_limpo(self):
        return _digits_only(getattr(self.request, "banco", "") or "")

    @property
    def db_alias(self):
        return getattr(self.request, "db_alias", None) or "default"

    def get_objeto_or_none(self):
        if not self.banco_limpo:
            return None
        return EventosAgrupadosService.obter(
            banco=self.banco_limpo,
            even_empr=self.EMPRESA_FIXA_CODIGO,
            even_fili=self.FILIAL_FIXA_CODIGO,
            db_alias=self.db_alias,
        )

    def get(self, request, *args, **kwargs):
        obj = self.get_objeto_or_none()
        if obj is None:
            messages.warning(request, "Configuração de eventos agrupados nao encontrada.")
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = self.get_objeto_or_none()
        if obj is None:
            return ctx
        ctx["object"] = obj
        ctx["objeto_desc"] = ""
        return ctx

    def post(self, request, *args, **kwargs):
        obj = self.get_objeto_or_none()
        if obj is None:
            messages.warning(request, "Configuração de eventos agrupados não encontrado.")
            return redirect(self.get_success_url())
        try:
            EventosAgrupadosService.excluir(
                banco=self.banco_limpo,
                even_empr=self.EMPRESA_FIXA_CODIGO,
                even_fili=self.FILIAL_FIXA_CODIGO,
                db_alias=self.db_alias,
            )
        except Exception as exc:
            messages.error(request, f"Não foi possivel excluir: {exc}")
            return redirect(self.get_success_url())
        messages.success(request, self.success_message)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url_name) + f"?banco={self.request.banco or 'rta0001'}"
