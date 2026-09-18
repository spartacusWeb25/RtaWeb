from horarios.models import Horarios
from django.db import connection


def _digits_only(valor) -> str:
    if valor is None:
        return ""
    return "".join(ch for ch in str(valor) if ch.isdigit())


_ORDENACAO_MAP = {
    "asc": "hora_codi ASC",
    "desc": "hora_codi DESC",
}


class ListarHorariosService:
    def listar(*, banco: str, db_alias: str, busca: str | None = None,
               ordenar: str | None = None):
        banco_limpo = _digits_only(banco)
        sql_base = (
            "SELECT registro, hora_empr, hora_fili, hora_codi, "
            "hora_nome, hora_total_semana, hora_flexivel "
            "FROM public.horarios WHERE registro=%s"
        )
        params = [banco_limpo]

        if busca:
            busca_stripped = busca.strip()
            if busca_stripped:
                eh_num = busca_stripped.isdigit()
                if eh_num:
                    sql_base += (
                        " AND (hora_codi = %s "
                        " OR hora_nome ILIKE %s )"
                    )
                    try:
                        params.append(int(busca_stripped))
                    except Exception:
                        params.append(0)
                    params.append(f"%{busca_stripped}%")
                else:
                    sql_base += " AND (hora_nome ILIKE %s)"
                    params.append(f"%{busca_stripped}%")

        ordem = _ORDENACAO_MAP.get((ordenar or "").lower(), _ORDENACAO_MAP["asc"])
        sql_base += f" ORDER BY {ordem}"

        with connection.cursor() as cursor:
            cursor.execute(sql_base, params)
            rows = cursor.fetchall()

        results = []
        colunas = [
            "registro", "hora_empr", "hora_fili", "hora_codi",
            "hora_nome", "hora_total_semana", "hora_flexivel",
        ]
        for row in rows:
            obj_dict = {}
            for i, col in enumerate(colunas):
                try:
                    obj_dict[col] = row[i]
                except IndexError:
                    obj_dict[col] = None
            results.append(type("HorarioRow", (), obj_dict)())
        return results
