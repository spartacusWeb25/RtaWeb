from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import UpdateView

from core.mixin import BancoObrigatorioMixin
from licencas.models import Usuarios
from licencas.services import UsuariosService
from licencas.web.forms import UsuarioLicencaForm


class UsuarioLicencaUpdateView(BancoObrigatorioMixin, UpdateView):
    model = Usuarios
    form_class = UsuarioLicencaForm
    template_name = "licencas/usuarios/form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Usuarios.objects.using("default"), id=self.kwargs["user_id"], registro=self.request.banco)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.registro = self.request.banco
        UsuariosService.salvar(instance=instance)
        messages.success(self.request, "Usuário atualizado com sucesso.")
        return redirect(reverse("licencas_usuarios:listar") + f"?banco={self.request.banco}")
