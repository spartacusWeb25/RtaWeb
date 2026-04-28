from django.shortcuts import render
from django.views import View

from core.mixin import BancoObrigatorioMixin
from tabelas.services.service_tabela_irrf import ServiceTabelaIrf


class TabelaIrrfSQLView(BancoObrigatorioMixin, View):
    def get(self, request):
        referencia = request.GET.get("ref")

        dados = None

        if referencia:
            dados = ServiceTabelaIrf._buscar_tabela_irrf(
                db_alias=request.db_alias,
                referencia=referencia,
            )

        context = {"registro": dados}

        return render(request, "tabelas/irrf_sql.html", context)
