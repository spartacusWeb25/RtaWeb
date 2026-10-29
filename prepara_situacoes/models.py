from django.db import connection, connections, models


_TABLE_COLUMNS_CACHE = {}


def _safe_int(value):
    try:
        if value is None:
            return None
        s = str(value).strip()
        if not s or not s.isdigit():
            return None
        return int(s)
    except Exception:
        return None


class PreparaSituacoes(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    prep_empr = models.IntegerField(blank=True, null=True)
    prep_fili = models.IntegerField(blank=True, null=True)
    prep_codi = models.IntegerField(blank=True, null=True)

    prep_desc = models.CharField(max_length=200, blank=True, null=True, default="")
    prep_descricao = models.CharField(max_length=250, blank=True, null=True, default="")

    prep_situacao_fixa = models.BooleanField(blank=True, null=True, default=False)
    prep_desc_situacao_folha = models.BooleanField(blank=True, null=True, default=False)
    prep_calcula_salario_familia = models.BooleanField(blank=True, null=True, default=False)
    prep_13_integral = models.BooleanField(blank=True, null=True, default=False)
    prep_reembolso_gps_13 = models.BooleanField(blank=True, null=True, default=False)
    prep_prorroga_periodo_aquisitivo = models.BooleanField(blank=True, null=True, default=False)
    prep_meses_media_sindicato = models.BooleanField(blank=True, null=True, default=False)
    prep_desc_tempo_servico = models.BooleanField(blank=True, null=True, default=False)
    prep_nao_prorroga_ult_prazo_ferias = models.BooleanField(blank=True, null=True, default=False)
    prep_perde_pa_afast_super_30 = models.BooleanField(blank=True, null=True, default=False)
    prep_ignora_inss_13 = models.BooleanField(blank=True, null=True, default=False)
    prep_ignora_ir_13 = models.BooleanField(blank=True, null=True, default=False)
    prep_ignora_fgts_13 = models.BooleanField(blank=True, null=True, default=False)

    prep_grupo_situacao = models.CharField(max_length=120, blank=True, null=True, default="")

    prep_usuario_inc = models.CharField(max_length=30, blank=True, null=True)
    prep_data_inc = models.DateField(blank=True, null=True)
    prep_usuario_alt = models.CharField(max_length=30, blank=True, null=True)
    prep_data_alt = models.DateField(blank=True, null=True)

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

        empr = _safe_int(getattr(self, "prep_empr", None))
        fili = _safe_int(getattr(self, "prep_fili", None))
        codi = _safe_int(getattr(self, "prep_codi", None))
        reg = str(getattr(self, "registro", "") or "")[:14]

        pk_exists = False
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM prepara_situacoes "
                    "WHERE registro = %s AND prep_empr = %s AND prep_fili = %s AND prep_codi = %s LIMIT 1",
                    [reg, empr, fili, codi],
                )
                pk_exists = bool(cur.fetchone())
        except Exception:
            qs = self.__class__.objects.using(using or "default").filter(
                registro=reg, prep_empr=empr, prep_fili=fili, prep_codi=codi,
            )
            pk_exists = qs.exists()

        if operacao == "criar" and pk_exists:
            raise RuntimeError(
                "[Protecao PK composta]: Tentativa de duplicar Preparacao de Situacao "
                f"reg={reg!r} empr={empr} fili={fili} cod={codi} que ja existe no banco."
            )

        pk_field_names = {"registro", "prep_empr", "prep_fili", "prep_codi"}
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
                'UPDATE prepara_situacoes SET ' + ', '.join(set_clause_parts)
                + ' WHERE "registro" = %s AND "prep_empr" = %s AND "prep_fili" = %s AND "prep_codi" = %s'
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
            'INSERT INTO prepara_situacoes (' + ', '.join(cols) + ') VALUES (' + ', '.join(placeholders) + ')'
        )
        with conn.cursor() as cur:
            cur.execute(sql_ins, params_ins)
        return self

    def delete(self, *args, **kwargs):
        using = kwargs.get("using") or self._state.db
        conn = self._get_connection(using)
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM prepara_situacoes '
                'WHERE "registro" = %s AND "prep_empr" = %s AND "prep_fili" = %s AND "prep_codi" = %s',
                [
                    str(getattr(self, "registro", "") or "")[:14],
                    _safe_int(getattr(self, "prep_empr", None)),
                    _safe_int(getattr(self, "prep_fili", None)),
                    _safe_int(getattr(self, "prep_codi", None)),
                ],
            )

    class Meta:
        managed = False
        db_table = "prepara_situacoes"
