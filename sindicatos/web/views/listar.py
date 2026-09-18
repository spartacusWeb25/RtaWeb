from django.views.generic import ListView
from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from sindicatos.models import Sindicatos
from sindicatos.services.listar import ListarSindicatosService


class SindicatoListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Sindicatos
    context_object_name = "sindicatos"
    template_name = "sindicatos/listar.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["referencia"] = self.request.GET.get("referencia", "")
        ctx["ordenar"] = self.request.GET.get("ordenar", "asc")
        return ctx

    def get_queryset(self):
        referencia = self.request.GET.get("referencia")
        ordenar = self.request.GET.get("ordenar", "asc")
        return ListarSindicatosService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
            ordenar=ordenar,
        )
