from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from licencas.models import Usuarios
from licencas.services import UsuariosService


class UsuariosListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Usuarios
    template_name = "licencas/usuarios/listar.html"
    context_object_name = "usuarios"
    paginate_by = 20

    def get_queryset(self):
        return UsuariosService.listar_por_registro(
            registro=self.request.banco,
            db_alias=self.request.db_alias,
            termo=self.request.GET.get("nome"),
            ordenar=self.request.GET.get("ordenar"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["banco"] = self.request.banco
        context["ordenar"] = self.request.GET.get("ordenar") or ""
        return context
