from tabelas.models import Tabelainssempresa


class ServiceTabelaInssEmpresa:
    @staticmethod
    def buscar_tabela_inss_empresa_queryset(*, db_alias, registro=None):
        qs = (
            Tabelainssempresa.objects
            .using(db_alias)
            .order_by("tabe_empr")
        )

        if registro:
            qs = qs.filter(registro=registro)

        return qs
