from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.mixin import BancoObrigatorioMixin
from licencas.models import Usuarios
from licencas.services import UsuariosService


class UsuarioLicencaDeleteView(BancoObrigatorioMixin, TemplateView):
    template_name = "licencas/usuarios/confirmar_exclusao.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["usuario"] = get_object_or_404(Usuarios.objects.using("default"), id=self.kwargs["user_id"], registro=self.request.banco)
        return context

    def post(self, request, *args, **kwargs):
        usuario = get_object_or_404(Usuarios.objects.using("default"), id=kwargs["user_id"], registro=request.banco)
        UsuariosService.remover(instance=usuario)
        messages.success(request, "Usuário excluído com sucesso.")
        return redirect(reverse("licencas_usuarios:listar") + f"?banco={request.banco}")
