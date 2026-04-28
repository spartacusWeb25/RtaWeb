from django.views import View
from django.shortcuts import render
from tabelas.services.service_tabela_irrf import ServiceTabelaIrf


class TabelaIrrfSQLView(View):

    def get(self, request):
        db_alias = request.GET.get("db", "default")
        referencia = request.GET.get("ref")

        dados = None

        if referencia:
            dados = ServiceTabelaIrf._buscar_tabela_irrf(
                db_alias=db_alias,
                referencia=referencia
            )

        context = {
            "registro": dados
        }

        return render(request, "tabelas/irrf_sql.html", context)