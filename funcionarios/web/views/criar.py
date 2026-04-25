from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from core.mixin import BancoObrigatorioMixin
from funcionarios.models import Funcionarios
from funcionarios.services import FuncionariosService
from funcionarios.web.forms import FuncionarioForm


class FuncionarioCreateView(BancoObrigatorioMixin, CreateView):
    model = Funcionarios
    form_class = FuncionarioForm
    template_name = "funcionarios/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.registro = self.request.banco
        FuncionariosService.salvar(instance=instance)
        messages.success(self.request, "Funcionário criado com sucesso.")
        return redirect(reverse("funcionarios:listar") + f"?banco={self.request.banco}")
