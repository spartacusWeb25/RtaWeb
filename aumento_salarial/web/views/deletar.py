from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from aumento_salarial.services.logic import AumentoSalarialService, _digits_only


class AumentoSalarialDeleteView(TemplateView):
    template_name = "aumento_salarial/confirmar_exclusao.html"
    success_url_name = "aumento_salarial:listar"
    success_message = "Aumento salarial excluido com sucesso."

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
        codi = int(self.kwargs.get("aume_codi") or 0)
        if not banco_limpo or not codi:
            return None
        return AumentoSalarialService.obter(
            banco=banco_limpo,
            aume_empr=self.EMPRESA_FIXA_CODIGO,
            aume_fili=self.FILIAL_FIXA_CODIGO,
            aume_codi=codi,
            db_alias=self.db_alias,
        )

    def get(self, request, *args, **kwargs):
        obj = self.get_objeto_or_none()
        if obj is None:
            messages.warning(request, "Aumento salarial nao encontrado.")
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = self.get_objeto_or_none()
        if obj is None:
            return ctx
        ctx["object"] = obj
        codigo = None
        try:
            codigo = int(getattr(obj, "aume_codi", None) or 0)
        except Exception:
            codigo = None
        descricao = str(getattr(obj, "aume_desc", None) or "").strip()
        partes = []
        if codigo:
            partes.append(f"Codigo {codigo}")
        if descricao:
            partes.append(descricao)
        ctx["objeto_desc"] = " - ".join(partes) if partes else "Aumento salarial"
        return ctx

    def post(self, request, *args, **kwargs):
        obj = self.get_objeto_or_none()
        if obj is None:
            messages.warning(request, "Aumento salarial nao encontrado.")
            return redirect(self.get_success_url())
        try:
            AumentoSalarialService.excluir(
                banco=self.banco_limpo,
                aume_empr=self.EMPRESA_FIXA_CODIGO,
                aume_fili=self.FILIAL_FIXA_CODIGO,
                aume_codi=int(getattr(obj, "aume_codi") or 0),
                db_alias=self.db_alias,
            )
        except Exception as exc:
            messages.error(request, f"Nao foi possivel excluir: {exc}")
            return redirect(self.get_success_url())
        messages.success(request, self.success_message)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url_name) + f"?banco={self.request.banco or 'rta0001'}"
