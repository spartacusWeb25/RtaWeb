from django.shortcuts import render
from django.views import View
from contribuintes.mixin import BancoObrigatorioMixin
from contribuintes.services.listar import listar_contribuintes


_ORDENACAO_MAP = {
    "asc": "codigo_crescente",
    "desc": "codigo_decrescente",
    "nome_asc": "nome_crescente",
    "nome_desc": "nome_decrescente",
}


class ContribuintesListView(BancoObrigatorioMixin, View):
    template_name = "contribuintes/listar.html"

    def get(self, request, *args, **kwargs):
        referencia = (request.GET.get("referencia") or request.GET.get("busca") or "").strip()
        ordenar = (request.GET.get("ordenar") or request.GET.get("ordenacao") or "asc").strip().lower()
        ordenacao_service = _ORDENACAO_MAP.get(ordenar, "codigo_crescente")
        lista = listar_contribuintes(request.banco, request.db_alias, referencia, ordenacao_service)
        return render(request, self.template_name, {
            "contribuintes": lista,
            "object_list": lista,
            "referencia": referencia,
            "busca": referencia,
            "ordenar": ordenar,
            "ordenacao": ordenacao_service,
            "breadcrumb": [{"nome": "Contribuintes"}],
            "page_title": "Contribuintes (Sócios / Diretores)",
        })
