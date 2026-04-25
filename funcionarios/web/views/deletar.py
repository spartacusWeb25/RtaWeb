from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.mixin import BancoObrigatorioMixin
from funcionarios.models import Funcionarios
from funcionarios.services import FuncionariosService


class FuncionarioDeleteView(BancoObrigatorioMixin, TemplateView):
    template_name = "funcionarios/confirmar_exclusao.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["funcionario"] = get_object_or_404(
            Funcionarios,
            registro=self.request.banco,
            func_codi=self.kwargs["func_codi"],
        )
        return context

    def post(self, request, *args, **kwargs):
        funcionario = get_object_or_404(
            Funcionarios,
            registro=request.banco,
            func_codi=kwargs["func_codi"],
        )
        FuncionariosService.remover(instance=funcionario)
        messages.success(request, "Funcionário removido com sucesso.")
        return redirect(reverse("funcionarios:listar") + f"?banco={request.banco}")
