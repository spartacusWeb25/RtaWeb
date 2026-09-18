from django.db import models
from django.db import connection

from core.consultas import BancoConsulta


class Sindicatos(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    sind_empr = models.IntegerField(blank=True, null=True)
    sind_fili = models.IntegerField(blank=True, null=True)
    sind_codi = models.IntegerField(blank=True, null=True)

    sind_nome = models.CharField(max_length=200, blank=True, null=True)
    sind_apelido = models.CharField(max_length=100, blank=True, null=True)
    sind_tipo_entidade = models.IntegerField(blank=True, null=True)
    sind_entidade = models.CharField(max_length=20, blank=True, null=True)
    sind_codi_sind = models.CharField(max_length=15, blank=True, null=True)
    sind_agencia_grcs = models.IntegerField(blank=True, null=True)
    sind_codi_cede = models.CharField(max_length=15, blank=True, null=True)
    sind_cep = models.CharField(max_length=8, blank=True, null=True)
    sind_logr = models.IntegerField(blank=True, null=True)
    sind_logr_desc = models.CharField(max_length=60, blank=True, null=True)
    sind_ende = models.CharField(max_length=120, blank=True, null=True)
    sind_ende_nume = models.CharField(max_length=20, blank=True, null=True)
    sind_ende_comp = models.CharField(max_length=60, blank=True, null=True)
    sind_ende_bair = models.CharField(max_length=60, blank=True, null=True)
    sind_cida_codi = models.IntegerField(blank=True, null=True)
    sind_cida_desc = models.CharField(max_length=60, blank=True, null=True)
    sind_esta = models.CharField(max_length=2, blank=True, null=True)
    sind_ddd1 = models.CharField(max_length=4, blank=True, null=True)
    sind_fone1 = models.CharField(max_length=20, blank=True, null=True)
    sind_ddd2 = models.CharField(max_length=4, blank=True, null=True)
    sind_fone2 = models.CharField(max_length=20, blank=True, null=True)
    sind_cnpj = models.CharField(max_length=14, blank=True, null=True)
    sind_tabela = models.IntegerField(blank=True, null=True)
    sind_site = models.CharField(max_length=150, blank=True, null=True)
    sind_emai = models.CharField(max_length=100, blank=True, null=True)

    # ============================================================
    # ABA 2: DADOS VARIÁVEIS MÊS A MÊS (26 campos)
    # ============================================================
    sind_dv_piso_salarial = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sind_dv_base_adicionais = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sind_dv_indice = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    sind_dv_maior_remuneracao = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sind_dv_maior_rem_agrupada = models.BooleanField(blank=True, null=True)
    sind_dv_aviso_previo_2anos = models.BooleanField(blank=True, null=True)
    sind_dv_perc_abono_ferias = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sind_dv_abono_sigla = models.CharField(max_length=3, blank=True, null=True)
    sind_dv_meses_ferias_dobro = models.IntegerField(blank=True, null=True)
    sind_dv_meses_ferias_justa = models.IntegerField(blank=True, null=True)
    sind_dv_ferias_rescisao = models.IntegerField(blank=True, null=True)
    sind_dv_perc_adicional_noturno = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sind_dv_data_base_mes = models.IntegerField(blank=True, null=True)
    sind_dv_estabilidade_dias = models.IntegerField(blank=True, null=True)
    sind_dv_liminar_aviso_codi = models.IntegerField(blank=True, null=True)
    sind_dv_liminar_aviso_13 = models.BooleanField(blank=True, null=True)
    sind_dv_verba_multa_codi = models.IntegerField(blank=True, null=True)
    sind_dv_verba_multa_desc = models.CharField(max_length=120, blank=True, null=True)
    sind_dv_mes_desc_sindical = models.IntegerField(blank=True, null=True)
    sind_dv_meses_homologacao = models.IntegerField(blank=True, null=True)
    sind_dv_mes_contribuicao_opcao = models.IntegerField(blank=True, null=True)
    sind_dv_hora_noturna_inicio = models.CharField(max_length=5, blank=True, null=True)
    sind_dv_hora_noturna_fim = models.CharField(max_length=5, blank=True, null=True)
    sind_dv_pagar_13_integral_bem = models.BooleanField(blank=True, null=True)
    sind_dv_nao_prorroga_aquisitivo_bem = models.BooleanField(blank=True, null=True)

    # ============================================================
    # ABA 3: MÉDIAS (49 campos)
    # ============================================================
    # Checkboxes topo
    sind_md_calc_maiores_meses_verba = models.BooleanField(blank=True, null=True)
    sind_md_calc_proporcional_verba = models.BooleanField(blank=True, null=True)

    # Médias para situação (3 linhas × 6 = 18 campos)
    # Cada: mes1 (SMALLINT), mes2 (SMALLINT), + val1-val4 (DECIMAL 12,2)
    sind_md_sit_rv_mes1 = models.IntegerField(blank=True, null=True)
    sind_md_sit_rv_mes2 = models.IntegerField(blank=True, null=True)
    sind_md_sit_rv_val1 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_sit_rv_val2 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_sit_rv_val3 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_sit_rv_val4 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    sind_md_sit_he_mes1 = models.IntegerField(blank=True, null=True)
    sind_md_sit_he_mes2 = models.IntegerField(blank=True, null=True)
    sind_md_sit_he_val1 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_sit_he_val2 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_sit_he_val3 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_sit_he_val4 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    sind_md_sit_hn_mes1 = models.IntegerField(blank=True, null=True)
    sind_md_sit_hn_mes2 = models.IntegerField(blank=True, null=True)
    sind_md_sit_hn_val1 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_sit_hn_val2 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_sit_hn_val3 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_sit_hn_val4 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Médias para férias + 13º (3 linhas × 6 = 18 campos + 2 check)
    sind_md_fer_rv_mes1 = models.IntegerField(blank=True, null=True)
    sind_md_fer_rv_mes2 = models.IntegerField(blank=True, null=True)
    sind_md_fer_rv_val1 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_fer_rv_val2 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_fer_rv_val3 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_fer_rv_val4 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    sind_md_fer_he_mes1 = models.IntegerField(blank=True, null=True)
    sind_md_fer_he_mes2 = models.IntegerField(blank=True, null=True)
    sind_md_fer_he_val1 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_fer_he_val2 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_fer_he_val3 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_fer_he_val4 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    sind_md_fer_hn_mes1 = models.IntegerField(blank=True, null=True)
    sind_md_fer_hn_mes2 = models.IntegerField(blank=True, null=True)
    sind_md_fer_hn_val1 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_fer_hn_val2 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_fer_hn_val3 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sind_md_fer_hn_val4 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    sind_md_fer_calc13_anterior = models.BooleanField(blank=True, null=True)
    sind_md_fer_calc_112_indeniz = models.BooleanField(blank=True, null=True)

    # Ignorar meses zerados (3 campos)
    sind_md_ign_rv = models.BooleanField(blank=True, null=True)
    sind_md_ign_he = models.BooleanField(blank=True, null=True)
    sind_md_ign_hn = models.BooleanField(blank=True, null=True)

    # Selects inferiores + checkbox
    sind_md_maiores_meses_opcao = models.IntegerField(blank=True, null=True)
    sind_md_maiores_meses_desc = models.CharField(max_length=120, blank=True, null=True)
    sind_md_media_ferias_codi = models.IntegerField(blank=True, null=True)
    sind_md_media_ferias_desc = models.CharField(max_length=200, blank=True, null=True)
    sind_md_media_ultimos_codi = models.IntegerField(blank=True, null=True)
    sind_md_media_ultimos_desc = models.CharField(max_length=200, blank=True, null=True)
    sind_md_incluir_mes_atual = models.BooleanField(blank=True, null=True)

    # ============================================================
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)

    objects = BancoConsulta()

    def __str__(self):
        return self.sind_nome or f"Sindicato #{self.sind_codi}"

    def _get_connection(self, using=None):
        alias = using or self._state.db or "default"
        try:
            from django.db import connections
            conn = connections[alias]
        except Exception:
            conn = connection
        return conn

    def save(self, *args, **kwargs):
        operacao = kwargs.pop("operacao", None)
        using = kwargs.get("using") or self._state.db
        conn = self._get_connection(using)

        empr = getattr(self, "sind_empr", None)
        fili = getattr(self, "sind_fili", None)
        codi = getattr(self, "sind_codi", None)
        reg = getattr(self, "registro", None)

        pk_exists = False
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM sindicatos WHERE registro = %s AND sind_empr = %s AND sind_fili = %s AND sind_codi = %s LIMIT 1",
                    [
                        str(reg or "")[:14],
                        int(empr) if str(empr or "").isdigit() else None,
                        int(fili) if str(fili or "").isdigit() else None,
                        int(codi) if str(codi or "").isdigit() else None,
                    ],
                )
                pk_exists = bool(cur.fetchone())
        except Exception:
            qs = self.__class__.objects.using(using or "default").filter(
                registro=self.registro, sind_empr=self.sind_empr,
                sind_fili=self.sind_fili, sind_codi=self.sind_codi,
            )
            pk_exists = qs.exists()

        if operacao == "criar" and pk_exists:
            raise RuntimeError(
                "[PROTECAO SOBRESCRITA ATIVADA]: Tentativa de INSERT duplicado em Sindicatos "
                f"com PK (registro={reg!r}, empr={empr}, fili={fili}, cod={codi}) que JA EXISTE no banco! "
                "Nao foi permitido sobrescrever o cadastro existente. Contate o suporte."
            )

        field_values = {}
        pk_field_names = {"registro", "sind_empr", "sind_fili", "sind_codi"}
        ordered_fields = []
        for field in self._meta.local_concrete_fields:
            ordered_fields.append(field)
            field_values[field.attname] = getattr(self, field.attname)

        if pk_exists:
            set_clause_parts = []
            params_update = []
            for field in ordered_fields:
                if field.attname in pk_field_names:
                    continue
                col = field.column
                set_clause_parts.append(f'"{col}" = %s')
                params_update.append(field_values[field.attname])
            params_update.extend([
                str(reg or "")[:14],
                int(empr) if str(empr or "").isdigit() else None,
                int(fili) if str(fili or "").isdigit() else None,
                int(codi) if str(codi or "").isdigit() else None,
            ])
            sql_update = (
                'UPDATE sindicatos SET ' + ', '.join(set_clause_parts)
                + ' WHERE "registro" = %s AND "sind_empr" = %s AND "sind_fili" = %s AND "sind_codi" = %s'
            )
            with conn.cursor() as cur:
                cur.execute(sql_update, params_update)
            return self

        cols = []
        placeholders = []
        params_insert = []
        for field in ordered_fields:
            cols.append(f'"{field.column}"')
            placeholders.append("%s")
            params_insert.append(field_values[field.attname])
        sql_insert = 'INSERT INTO sindicatos (' + ', '.join(cols) + ') VALUES (' + ', '.join(placeholders) + ')'
        with conn.cursor() as cur:
            cur.execute(sql_insert, params_insert)
        return self

    def delete(self, *args, **kwargs):
        using = kwargs.get("using") or self._state.db
        conn = self._get_connection(using)
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM sindicatos WHERE "registro" = %s AND "sind_empr" = %s AND "sind_fili" = %s AND "sind_codi" = %s',
                [
                    str(getattr(self, "registro", None) or "")[:14],
                    int(getattr(self, "sind_empr")) if str(getattr(self, "sind_empr") or "").isdigit() else None,
                    int(getattr(self, "sind_fili")) if str(getattr(self, "sind_fili") or "").isdigit() else None,
                    int(getattr(self, "sind_codi")) if str(getattr(self, "sind_codi") or "").isdigit() else None,
                ],
            )

    class Meta:
        managed = False
        db_table = 'sindicatos'
        unique_together = (('registro', 'sind_empr', 'sind_fili', 'sind_codi'),)
