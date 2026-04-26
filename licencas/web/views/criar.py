from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from core.mixin import BancoObrigatorioMixin
from licencas.models import Usuarios
from licencas.services import UsuariosService
from licencas.web.forms import UsuariosForm


class UsuariosCreateView(BancoObrigatorioMixin, CreateView):
    model = Usuarios
    form_class = UsuariosForm
    template_name = "licencas/usuarios/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.registro = self.request.banco
        UsuariosService.salvar(instance=instance)
        messages.success(self.request, "Usuário criado com sucesso.")
        return redirect(reverse("licencas:listar") + f"?banco={self.request.banco}")
