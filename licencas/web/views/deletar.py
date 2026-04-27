from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.mixin import BancoObrigatorioMixin
from licencas.services import UsuariosService


class UsuariosDeleteView(BancoObrigatorioMixin, TemplateView):
    template_name = "licencas/usuarios/confirmar_exclusao.html"

    def _get_usuario(self, user_id):
        usuario = UsuariosService.buscar(
            registro=self.request.banco,
            user_id=user_id,
            db_alias=self.request.db_alias,
        )
        if not usuario:
            raise Http404("Usuário não encontrado.")
        return usuario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["usuario"] = self._get_usuario(user_id=self.kwargs["user_id"])
        return context

    def post(self, request, *args, **kwargs):
        usuario = self._get_usuario(user_id=kwargs["user_id"])
        UsuariosService.remover(instance=usuario, db_alias=request.db_alias)
        messages.success(request, "Usuário excluído com sucesso.")
        return redirect(reverse("licencas:listar") + f"?banco={request.banco}")
