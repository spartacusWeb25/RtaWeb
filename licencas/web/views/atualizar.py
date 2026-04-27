from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView

from core.mixin import BancoObrigatorioMixin
from licencas.models import Usuarios
from licencas.services import UsuariosService
from licencas.web.forms import UsuariosForm


class UsuariosUpdateView(BancoObrigatorioMixin, UpdateView):
    model = Usuarios
    form_class = UsuariosForm   
    template_name = "licencas/usuarios/form.html"

    def get_object(self, queryset=None):
        usuario = UsuariosService.buscar(
            registro=self.request.banco,
            user_id=self.kwargs["user_id"],   
            db_alias=self.request.db_alias,
        )
        if not usuario:
            raise Http404("Usuário não encontrado.")
        return usuario

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.registro = self.request.banco
        UsuariosService.salvar(instance=instance, db_alias=self.request.db_alias)
        messages.success(self.request, "Usuário atualizado com sucesso.")
        return redirect(reverse("usuarios:listar") + f"?banco={self.request.banco}")
