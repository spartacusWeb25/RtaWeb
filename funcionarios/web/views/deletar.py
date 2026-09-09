from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.mixin import BancoObrigatorioMixin
from funcionarios.models import Funcionarios
from funcionarios.services import FuncionariosService


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


class FuncionarioDeleteView(BancoObrigatorioMixin, TemplateView):
    template_name = "funcionarios/confirmar_exclusao.html"

    def get_funcionario(self):
        banco_limpo = _digits_only(self.request.banco)
        funcionario = (
            self.get_queryset()
            .filter(
                registro=banco_limpo,
                func_empr=self.kwargs["func_empr"],
                func_fili=self.kwargs["func_fili"],
                func_codi=self.kwargs["func_codi"],
            )
            .first()
        )
        if funcionario is None:
            raise Http404
        return funcionario

    def get_queryset(self):
        banco_limpo = _digits_only(self.request.banco)
        return Funcionarios.objects.using(self.request.db_alias).filter(
            registro=banco_limpo
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_funcionario()
        context["funcionario"] = obj
        context["object"] = obj
        return context

    def post(self, request, *args, **kwargs):
        banco_limpo = _digits_only(request.banco)
        funcionario = self.get_funcionario()
        FuncionariosService.remover(
            banco=banco_limpo,
            instance=funcionario,
        )
        messages.success(request, "Funcionário removido com sucesso.")
        return redirect(reverse("funcionarios:listar") + f"?banco={banco_limpo}")
