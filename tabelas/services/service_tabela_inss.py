from tabelas.models import Tabelainss


class ServiceTabelaInss:
    @staticmethod
    def buscar_tabela_inss_queryset(*, db_alias, referencia=None):
        qs = (
            Tabelainss.objects
            .using(db_alias)
            .order_by("-tabe_refe")
        )

        if referencia:
            qs = qs.filter(tabe_refe__lte=referencia)

        return qs
