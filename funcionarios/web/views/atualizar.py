from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView

from core.mixin import BancoObrigatorioMixin
from funcionarios.models import Funcionarios
from funcionarios.services import FuncionariosService
from funcionarios.web.forms import FuncionarioForm


class FuncionarioUpdateView(BancoObrigatorioMixin, UpdateView):
    model = Funcionarios
    form_class = FuncionarioForm
    template_name = "funcionarios/form.html"
    context_object_name = "funcionario"

    def get_object(self, queryset=None):
        return self.get_contextual_object(
            Funcionarios.objects,
            func_codi=self.kwargs["func_codi"],
        )

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.registro = self.request.banco
        FuncionariosService.salvar(instance=instance)
        messages.success(self.request, "Funcionário atualizado com sucesso.")
        return redirect(reverse("funcionarios:listar") + f"?banco={self.request.banco}")
