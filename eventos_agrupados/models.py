from django.db import connection, connections, models


_TABLE_COLUMNS_CACHE = {}


def _safe_int(value):
    try:
        if value is None:
            return None
        text = str(value).strip()
        if not text or not text.isdigit():
            return None
        return int(text)
    except Exception:
        return None


class EventosAgrupados(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    even_empr = models.IntegerField(blank=True, null=True)
    even_fili = models.IntegerField(blank=True, null=True)

    even_ferias_proporcionais = models.IntegerField(blank=True, null=True)
    even_ferias_vencidas = models.IntegerField(blank=True, null=True)
    even_ferias_dobro = models.IntegerField(blank=True, null=True)
    even_ferias_indenizadas = models.IntegerField(blank=True, null=True)
    even_13_salario = models.IntegerField(blank=True, null=True)
    even_13_salario_indenizado = models.IntegerField(blank=True, null=True)
    even_aviso_previo_indenizado = models.IntegerField(blank=True, null=True)

    def _get_connection(self, using=None):
        try:
            alias = using or "default"
            return connections[alias]
        except Exception:
            return connection

    def _get_table_columns(self, conn):
        alias = getattr(conn, "alias", None) or "default"
        cache_key = (alias, self._meta.db_table)
        if cache_key in _TABLE_COLUMNS_CACHE:
            return _TABLE_COLUMNS_CACHE[cache_key]
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT column_name "
                    "FROM information_schema.columns "
                    "WHERE table_schema = 'public' AND table_name = %s",
                    [self._meta.db_table],
                )
                cols = {row[0] for row in (cur.fetchall() or [])}
        except Exception:
            cols = set()
        _TABLE_COLUMNS_CACHE[cache_key] = cols
        return cols

    def save(self, *args, **kwargs):
        operacao = kwargs.pop("operacao", None)
        using = kwargs.get("using") or self._state.db
        conn = self._get_connection(using)

        reg = str(getattr(self, "registro", "") or "")[:14]
        empr = _safe_int(getattr(self, "even_empr", None))
        fili = _safe_int(getattr(self, "even_fili", None))

        pk_exists = False
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM eventos_agrupados "
                    "WHERE registro = %s AND even_empr = %s AND even_fili = %s LIMIT 1",
                    [reg, empr, fili],
                )
                pk_exists = bool(cur.fetchone())
        except Exception:
            qs = self.__class__.objects.using(using or "default").filter(
                registro=reg,
                even_empr=empr,
                even_fili=fili,
            )
            pk_exists = qs.exists()

        if operacao == "criar" and pk_exists:
            raise RuntimeError(
                "[Protecao PK composta]: Tentativa de duplicar Eventos Agrupados "
                f"reg={reg!r} empr={empr} fili={fili} que ja existe no banco."
            )

        pk_field_names = {"registro", "even_empr", "even_fili"}
        ordered_fields = []
        field_values = {}
        table_columns = self._get_table_columns(conn)
        for field in self._meta.local_concrete_fields:
            if table_columns and field.column not in table_columns:
                continue
            ordered_fields.append(field)
            field_values[field.attname] = getattr(self, field.attname)

        if pk_exists:
            set_clause_parts = []
            params_upd = []
            for field in ordered_fields:
                if field.attname in pk_field_names:
                    continue
                set_clause_parts.append(f'"{field.column}" = %s')
                params_upd.append(field_values[field.attname])
            params_upd.extend([reg, empr, fili])
            sql_upd = (
                'UPDATE eventos_agrupados SET ' + ', '.join(set_clause_parts)
                + ' WHERE "registro" = %s AND "even_empr" = %s AND "even_fili" = %s'
            )
            with conn.cursor() as cur:
                cur.execute(sql_upd, params_upd)
            return self

        cols = []
        placeholders = []
        params_ins = []
        for field in ordered_fields:
            cols.append(f'"{field.column}"')
            placeholders.append("%s")
            params_ins.append(field_values[field.attname])
        sql_ins = (
            'INSERT INTO eventos_agrupados (' + ', '.join(cols) + ') VALUES (' + ', '.join(placeholders) + ')'
        )
        with conn.cursor() as cur:
            cur.execute(sql_ins, params_ins)
        return self

    def delete(self, *args, **kwargs):
        using = kwargs.get("using") or self._state.db
        conn = self._get_connection(using)
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM eventos_agrupados '
                'WHERE "registro" = %s AND "even_empr" = %s AND "even_fili" = %s',
                [
                    str(getattr(self, "registro", "") or "")[:14],
                    _safe_int(getattr(self, "even_empr", None)),
                    _safe_int(getattr(self, "even_fili", None)),
                ],
            )

    class Meta:
        managed = False
        db_table = "eventos_agrupados"
