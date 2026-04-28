from django.db import connections
from tabelas.models import Tabelairrf


class ServiceTabelaIrf:

    @staticmethod
    def _buscar_tabela_irrf(*, db_alias, referencia):
            with connections[db_alias].cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM tabelairrf
                    WHERE irrf_refe <= %s
                    ORDER BY irrf_refe DESC
                    LIMIT 1
                    """,
                    [referencia],
                )
                row = cursor.fetchone()
                if not row:
                    return None

                cols = [col[0] for col in cursor.description]
                return dict(zip(cols, row))
    
    @staticmethod
    def buscar_tabela_irrf_queryset(*, db_alias, referencia):
        qs = (
            Tabelairrf.objects
            .using(db_alias)
            .order_by("-irrf_refe")
        )

        if referencia:
            qs = qs.filter(irrf_refe__lte=referencia)

        return qs