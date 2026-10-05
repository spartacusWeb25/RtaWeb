from django.db import models, connection, connections


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


class PreparaRescisoes(models.Model):
    # ============================================================
    # CHAVE PRIMÁRIA COMPOSTA REAL 4 colunas (padrão projeto legado)
    # ============================================================
    registro = models.CharField(primary_key=True, max_length=14)
    prep_empr = models.IntegerField(blank=True, null=True)
    prep_fili = models.IntegerField(blank=True, null=True)
    prep_codi = models.IntegerField(blank=True, null=True)

    # ============================================================
    # ABA 1: BÁSICOS (Código + Descrição + Inativo)
    # ============================================================
    prep_desc = models.CharField(max_length=200, blank=True, null=True, default='', verbose_name="Descrição (título)")
    prep_descricao = models.CharField(max_length=200, blank=True, null=True, default='', verbose_name="Descrição")
    prep_inativo = models.BooleanField(blank=True, null=True, default=False, verbose_name="Inativo")

    # ============================================================
    # ABA 2: DADOS GERAIS (superior da tela SCI)
    # ============================================================
    prep_iniciativa_codi = models.IntegerField(blank=True, null=True, verbose_name="Iniciativa (código)")
    prep_iniciativa_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="Iniciativa (descrição)")

    prep_aviso_previo_codi = models.IntegerField(blank=True, null=True, verbose_name="Aviso prévio (código)")
    prep_aviso_previo_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="Aviso prévio")
    prep_inden_ferias_13 = models.BooleanField(blank=True, null=True, default=False, verbose_name="Indenização 1/12 férias e 13º")

    prep_saque_codi = models.CharField(max_length=20, blank=True, null=True, verbose_name="Código saque")
    prep_saque_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="Código saque (descrição)")

    prep_fgts_codi = models.CharField(max_length=20, blank=True, null=True, verbose_name="FGTS")
    prep_fgts_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="FGTS (descrição)")

    prep_fgts_int_codi = models.CharField(max_length=20, blank=True, null=True, verbose_name="FGTS intermitente")
    prep_fgts_int_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="FGTS intermitente (descrição)")

    prep_caged_codi = models.CharField(max_length=20, blank=True, null=True, verbose_name="CAGED")
    prep_caged_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="CAGED (descrição)")
    prep_rais_codi = models.CharField(max_length=20, blank=True, null=True, verbose_name="RAIS")
    prep_rais_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="RAIS (descrição)")

    prep_gfd_codi = models.IntegerField(blank=True, null=True, verbose_name="GFD / GRRF (código)")
    prep_gfd_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="GFD / GRRF (descrição)")

    prep_homolognet_codi = models.CharField(max_length=20, blank=True, null=True, verbose_name="Código HomologNet")
    prep_homolognet_desc = models.CharField(max_length=250, blank=True, null=True, verbose_name="HomologNet (descrição)")

    prep_motivo_esocial_codi = models.CharField(max_length=20, blank=True, null=True, verbose_name="Motivo eSocial")
    prep_motivo_esocial_desc = models.CharField(max_length=250, blank=True, null=True, verbose_name="Motivo eSocial (descrição)")

    # ============================================================
    # ABA 3: CHECKBOXES INFERIORES (inferior tela SCI)
    # ============================================================
    prep_justa_causa = models.BooleanField(blank=True, null=True, default=False, verbose_name="Justa causa")
    prep_inden_contr_exp = models.BooleanField(blank=True, null=True, default=False, verbose_name="Indenização contrato experiência")
    prep_emitir_seg_desemp = models.BooleanField(blank=True, null=True, default=False, verbose_name="Emitir seguro desemprego")
    prep_50_aviso_inden = models.BooleanField(blank=True, null=True, default=False, verbose_name="50% do aviso indenizado")
    prep_estabilidade = models.BooleanField(blank=True, null=True, default=False, verbose_name="Estabilidade")
    prep_nao_calc_multa_resc = models.BooleanField(blank=True, null=True, default=False, verbose_name="Não calcula multa rescisória")
    prep_50_verbas_inden = models.BooleanField(blank=True, null=True, default=False, verbose_name="50% das verbas indenizadas (aviso/férias/13º)")

    prep_rescisao_fixa = models.BooleanField(blank=True, null=True, default=False, verbose_name="Rescisão fixa")

    # ============================================================
    # LOGS (padrão projeto)
    # ============================================================
    prep_usuario_inc = models.CharField(max_length=30, blank=True, null=True)
    prep_data_inc = models.DateField(blank=True, null=True)
    prep_usuario_alt = models.CharField(max_length=30, blank=True, null=True)
    prep_data_alt = models.DateField(blank=True, null=True)

    # ============================================================
    # Métodos internos: raw save / raw delete via SQL (PK composta)
    # ============================================================
    def _get_connection(self, using=None):
        try:
            alias = using or "default"
            return connections[alias]
        except Exception:
            return connection

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
                    "SELECT 1 FROM prepara_rescisoes "
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
                "[Proteção PK composta]: Tentativa de duplicar Preparação de Rescisão "
                f"reg={reg!r} empr={empr} fili={fili} cod={codi} que já existe no banco."
            )

        pk_field_names = {"registro", "prep_empr", "prep_fili", "prep_codi"}
        ordered_fields = []
        field_values = {}
        for field in self._meta.local_concrete_fields:
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
                'UPDATE prepara_rescisoes SET ' + ', '.join(set_clause_parts)
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
            'INSERT INTO prepara_rescisoes (' + ', '.join(cols) + ') VALUES (' + ', '.join(placeholders) + ')'
        )
        with conn.cursor() as cur:
            cur.execute(sql_ins, params_ins)
        return self

    def delete(self, *args, **kwargs):
        using = kwargs.get("using") or self._state.db
        conn = self._get_connection(using)
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM prepara_rescisoes '
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
        db_table = 'prepara_rescisoes'
