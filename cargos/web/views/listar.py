from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin
from cargos.models import Cargos
from cargos.services.listar import ListarCargosService
from cargos.services.logic import _digits_only


class CargosListView(BancoObrigatorioMixin, ListView):
    model = Cargos
    template_name = "cargos/listar.html"
    context_object_name = "cargos"
    paginate_by = 30

    def get_queryset(self):
        referencia = self.request.GET.get("referencia")
        ordenar = self.request.GET.get("ordenar", "asc")
        return ListarCargosService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
            ordenar=ordenar,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["banco_limpo"] = _digits_only(getattr(self.request, "banco", "") or "")
        ctx["ordenar"] = self.request.GET.get("ordenar", "asc")
        return ctx
