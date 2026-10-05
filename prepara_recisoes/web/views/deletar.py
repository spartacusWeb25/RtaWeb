from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from prepara_recisoes.services.logic import PreparaRescisoesService, _digits_only
from prepara_recisoes.models import PreparaRescisoes


class PreparaRescisoesDeleteView(TemplateView):
    template_name = "prepara_recisoes/confirmar_exclusao.html"
    success_url_name = "prepara_recisoes:listar"
    success_message = "Preparação de rescisão excluída com sucesso."

    EMPRESA_FIXA_CODIGO = 1
    FILIAL_FIXA_CODIGO = 1

    @property
    def banco_limpo(self):
        return _digits_only(getattr(self.request, "banco", "") or "")

    @property
    def db_alias(self):
        return getattr(self.request, "db_alias", None) or "default"

    def get_objeto_or_none(self):
        banco_limpo = self.banco_limpo
        codi = int(self.kwargs.get("prep_codi") or 0)
        if not banco_limpo or not codi:
            return None
        return (
            PreparaRescisoes.objects.using(self.db_alias)
            .filter(
                registro=banco_limpo,
                prep_empr=self.EMPRESA_FIXA_CODIGO,
                prep_fili=self.FILIAL_FIXA_CODIGO,
                prep_codi=codi,
            )
            .first()
        )

    def get(self, request, *args, **kwargs):
        obj = self.get_objeto_or_none()
        if obj is None:
            messages.warning(
                request,
                "Preparação de Rescisão não encontrada (já foi excluída ou não existe)."
            )
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = self.get_objeto_or_none()
        if obj is None:
            return ctx
        ctx["object"] = obj
        codigo = None
        descricao = ""
        try:
            codigo = int(getattr(obj, "prep_codi", None) or 0)
        except Exception:
            codigo = None
        descricao = (
            str(getattr(obj, "prep_desc", None) or "").strip()
            or str(getattr(obj, "prep_descricao", None) or "").strip()
        )
        partes = []
        if codigo:
            partes.append(f"Código {codigo}")
        if descricao:
            partes.append(descricao)
        ctx["objeto_desc"] = " — ".join(partes) if partes else "Preparação de Rescisão"
        ctx["objeto_id"] = codigo
        ctx["objeto_descricao"] = descricao
        return ctx

    def post(self, request, *args, **kwargs):
        obj = self.get_objeto_or_none()
        if obj is None:
            messages.warning(
                request,
                "Preparação de Rescisão não encontrada (já foi excluída ou não existe)."
            )
            return redirect(self.get_success_url())
        try:
            PreparaRescisoesService.excluir(
                banco=self.banco_limpo,
                prep_empr=self.EMPRESA_FIXA_CODIGO,
                prep_fili=self.FILIAL_FIXA_CODIGO,
                prep_codi=int(getattr(obj, "prep_codi") or 0),
                db_alias=self.db_alias,
            )
        except Exception as exc:
            messages.error(request, f"Não foi possível excluir: {exc}")
            return redirect(self.get_success_url())
        messages.success(request, self.success_message)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url_name) + f"?banco={self.request.banco or 'rta0001'}"
