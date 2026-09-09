from django.views.generic import ListView
from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from ...models import Eventos
from eventos.services.listar import ListarEventosService

class EventosListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Eventos
    template_name = "eventos/listar.html"
    context_object_name = "eventos"
    paginate_by = 20
    
    def get_queryset(self):
        referencia = self.request.GET.get("referencia")
        ordenar = self.request.GET.get("ordenar")
        return ListarEventosService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
            ordenar=ordenar,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["referencia"] = self.request.GET.get("referencia", "")
        context["ordenar"] = self.request.GET.get("ordenar", "")
        return context
