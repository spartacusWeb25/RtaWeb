from django.shortcuts import render
from django.views import View
from sindicatospatronais.mixin import SindPatronalMixin
from sindicatospatronais.services.listar import ListarSindicatosPatronaisService


_ORDENACAO_MAP = {
    "asc": "codigo_crescente",
    "desc": "codigo_decrescente",
}


class SindicatosPatronaisListView(SindPatronalMixin, View):
    template_name = "sindicatospatronais/listar.html"

    def get(self, request, *args, **kwargs):
        referencia = (request.GET.get("referencia") or request.GET.get("busca") or "").strip()
        ordenar = (request.GET.get("ordenar") or request.GET.get("ordenacao") or "asc").strip().lower()
        ordenacao_service = _ORDENACAO_MAP.get(ordenar, "codigo_crescente")
        lista = ListarSindicatosPatronaisService.listar(
            banco=request.banco,
            db_alias=request.db_alias,
            referencia=referencia,
            ordenacao=ordenacao_service,
        )
        return render(request, self.template_name, {
            "lista": lista,
            "object_list": lista,
            "sindicatospatronais": lista,
            "referencia": referencia,
            "busca": referencia,
            "ordenar": ordenar,
            "ordenacao": ordenacao_service,
            "banco": request.banco,
            "breadcrumb": [{"nome": "Sindicatos Patronais"}],
            "page_title": "Sindicatos Patronais",
        })
