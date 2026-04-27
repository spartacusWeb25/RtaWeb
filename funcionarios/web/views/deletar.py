from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.mixin import BancoObrigatorioMixin
from funcionarios.services import FuncionariosService


class FuncionarioDeleteView(BancoObrigatorioMixin, TemplateView):
    template_name = "funcionarios/confirmar_exclusao.html"

    def get_funcionario(self):
        return self.get_contextual_object(
            self.get_queryset(),
            func_codi=self.kwargs["func_codi"],
        )

    def get_queryset(self):
        return FuncionariosService.listar_por_banco(banco=self.request.banco)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["funcionario"] = self.get_funcionario()
        return context

    def post(self, request, *args, **kwargs):
        funcionario = self.get_funcionario()
        FuncionariosService.remover(instance=funcionario)
        messages.success(request, "Funcionário removido com sucesso.")
        return redirect(reverse("funcionarios:listar") + f"?banco={request.banco}")
