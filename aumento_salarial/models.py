from django.db import connection, connections, models


_TABLE_COLUMNS_CACHE = {}


def _safe_int(value):
    try:
        if value is None:
            return None
        text = str(value).strip()
        if not text or not text.lstrip("-").isdigit():
            return None
        return int(text)
    except Exception:
        return None


class AumentoSalarial(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    aume_empr = models.IntegerField(blank=True, null=True)
    aume_fili = models.IntegerField(blank=True, null=True)
    aume_codi = models.IntegerField(blank=True, null=True)

    aume_desc = models.CharField(max_length=200, blank=True, null=True, default="")
    aume_func = models.IntegerField(blank=True, null=True)
    aume_data_alteracao = models.DateField(blank=True, null=True)
    aume_data_efeito = models.DateField(blank=True, null=True)
    aume_motivo = models.CharField(max_length=200, blank=True, null=True, default="")
    aume_forma = models.CharField(max_length=1, blank=True, null=True, default="")
    aume_valor = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    aume_contribuintes = models.BooleanField(blank=True, null=True, default=False)
    aume_tipo_funcionario = models.CharField(max_length=1, blank=True, null=True, default="")
    aume_classe = models.IntegerField(blank=True, null=True)
    aume_cargo = models.IntegerField(blank=True, null=True)
    aume_departamento = models.IntegerField(blank=True, null=True)
    aume_centro_custo = models.IntegerField(blank=True, null=True)
    aume_sindicato = models.IntegerField(blank=True, null=True)
    aume_salario_atual = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    aume_aumento_proporcional = models.BooleanField(blank=True, null=True, default=False)
    aume_arredondar_salario = models.BooleanField(blank=True, null=True, default=False)
    aume_alterar_meses_posteriores = models.BooleanField(blank=True, null=True, default=False)
    aume_demitidos_mes = models.BooleanField(blank=True, null=True, default=False)
    aume_admitidos_mes = models.BooleanField(blank=True, null=True, default=False)

    aume_usuario_inc = models.CharField(max_length=30, blank=True, null=True)
    aume_data_inc = models.DateField(blank=True, null=True)
    aume_usuario_alt = models.CharField(max_length=30, blank=True, null=True)
    aume_data_alt = models.DateField(blank=True, null=True)
    log_data = models.DateField(db_column="_log_data", blank=True, null=True)
    log_hora = models.TimeField(db_column="_log_time", blank=True, null=True)

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
        empr = _safe_int(getattr(self, "aume_empr", None))
        fili = _safe_int(getattr(self, "aume_fili", None))
        codi = _safe_int(getattr(self, "aume_codi", None))

        pk_exists = False
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM aumento_salarial "
                    "WHERE registro = %s AND aume_empr = %s AND aume_fili = %s AND aume_codi = %s LIMIT 1",
                    [reg, empr, fili, codi],
                )
                pk_exists = bool(cur.fetchone())
        except Exception:
            qs = self.__class__.objects.using(using or "default").filter(
                registro=reg,
                aume_empr=empr,
                aume_fili=fili,
                aume_codi=codi,
            )
            pk_exists = qs.exists()

        if operacao == "criar" and pk_exists:
            raise RuntimeError(
                "[Protecao PK composta]: Tentativa de duplicar Aumento Salarial "
                f"reg={reg!r} empr={empr} fili={fili} cod={codi} que ja existe no banco."
            )

        pk_field_names = {"registro", "aume_empr", "aume_fili", "aume_codi"}
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
            params_upd.extend([reg, empr, fili, codi])
            sql_upd = (
                'UPDATE aumento_salarial SET ' + ', '.join(set_clause_parts)
                + ' WHERE "registro" = %s AND "aume_empr" = %s AND "aume_fili" = %s AND "aume_codi" = %s'
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
            'INSERT INTO aumento_salarial (' + ', '.join(cols) + ') VALUES (' + ', '.join(placeholders) + ')'
        )
        with conn.cursor() as cur:
            cur.execute(sql_ins, params_ins)
        return self

    def delete(self, *args, **kwargs):
        using = kwargs.get("using") or self._state.db
        conn = self._get_connection(using)
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM aumento_salarial '
                'WHERE "registro" = %s AND "aume_empr" = %s AND "aume_fili" = %s AND "aume_codi" = %s',
                [
                    str(getattr(self, "registro", "") or "")[:14],
                    _safe_int(getattr(self, "aume_empr", None)),
                    _safe_int(getattr(self, "aume_fili", None)),
                    _safe_int(getattr(self, "aume_codi", None)),
                ],
            )

    class Meta:
        managed = False
        db_table = "aumento_salarial"
        unique_together = (("registro", "aume_empr", "aume_fili", "aume_codi"),)
