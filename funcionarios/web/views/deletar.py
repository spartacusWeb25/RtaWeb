from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.mixin import BancoObrigatorioMixin
from funcionarios.models import Funcionarios
from funcionarios.services import FuncionariosService


class FuncionarioDeleteView(BancoObrigatorioMixin, TemplateView):
    template_name = "funcionarios/confirmar_exclusao.html"

    def get_funcionario(self):
        funcionario = (
            self.get_queryset()
            .filter(
                registro=self.request.banco,
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
        return Funcionarios.objects.using(self.request.db_alias).filter(
            registro=self.request.banco
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["funcionario"] = self.get_funcionario()
        return context

    def post(self, request, *args, **kwargs):
        funcionario = self.get_funcionario()
        FuncionariosService.remover(
            banco=request.banco,
            instance=funcionario,
        )
        messages.success(request, "Funcionário removido com sucesso.")
        return redirect(reverse("funcionarios:listar") + f"?banco={request.banco}")
