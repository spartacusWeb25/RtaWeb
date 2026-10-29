from types import SimpleNamespace

from django.urls import reverse
from django.views.generic import ListView

from eventos_agrupados.mixin import EventosAgrupadosMixin
from eventos_agrupados.services.logic import EventosAgrupadosService


class EventosAgrupadosListView(EventosAgrupadosMixin, ListView):
    model = None
    template_name = "eventos_agrupados/listar.html"
    context_object_name = "objetos"

    def get_queryset(self):
        itens = EventosAgrupadosService.listar(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=self.EMPRESA_FIXA_CODIGO,
            codigo_filial=self.FILIAL_FIXA_CODIGO,
        )
        return [SimpleNamespace(**item) for item in itens]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Eventos agrupados para cálculo"
        ctx["url_novo"] = reverse("eventos_agrupados:criar") + f"?banco={self.request.banco or ''}"
        ctx["tem_configuracao"] = bool(ctx.get("objetos"))
        return ctx
