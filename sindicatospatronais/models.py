from django.db import models
from django.db import connection

from core.consultas import BancoConsulta


class SindicatosPatronais(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    sind_empr = models.IntegerField(blank=True, null=True)
    sind_fili = models.IntegerField(blank=True, null=True)
    sind_codi = models.IntegerField(blank=True, null=True)

    sind_nome = models.CharField(max_length=200, blank=True, null=True)
    sind_tipo_entidade = models.IntegerField(blank=True, null=True)
    sind_entidade = models.CharField(max_length=20, blank=True, null=True)
    sind_codi_sind = models.CharField(max_length=15, blank=True, null=True)
    sind_agencia_grcs = models.IntegerField(blank=True, null=True)
    sind_codi_cede = models.CharField(max_length=15, blank=True, null=True)
    sind_cep = models.CharField(max_length=8, blank=True, null=True)
    sind_logr = models.IntegerField(blank=True, null=True)
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
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)

    objects = BancoConsulta()

    def __str__(self):
        return self.sind_nome or f"Sind. Patronal #{self.sind_codi}"

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
                    "SELECT 1 FROM sindicatospatronais WHERE registro = %s AND sind_empr = %s AND sind_fili = %s AND sind_codi = %s LIMIT 1",
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
                "[PROTECAO SOBRESCRITA ATIVADA]: Tentativa de INSERT duplicado em SindicatosPatronais "
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
                'UPDATE sindicatospatronais SET ' + ', '.join(set_clause_parts)
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
        sql_insert = 'INSERT INTO sindicatospatronais (' + ', '.join(cols) + ') VALUES (' + ', '.join(placeholders) + ')'
        with conn.cursor() as cur:
            cur.execute(sql_insert, params_insert)
        return self

    def delete(self, *args, **kwargs):
        using = kwargs.get("using") or self._state.db
        conn = self._get_connection(using)
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM sindicatospatronais WHERE "registro" = %s AND "sind_empr" = %s AND "sind_fili" = %s AND "sind_codi" = %s',
                [
                    str(getattr(self, "registro", None) or "")[:14],
                    int(getattr(self, "sind_empr")) if str(getattr(self, "sind_empr") or "").isdigit() else None,
                    int(getattr(self, "sind_fili")) if str(getattr(self, "sind_fili") or "").isdigit() else None,
                    int(getattr(self, "sind_codi")) if str(getattr(self, "sind_codi") or "").isdigit() else None,
                ],
            )

    class Meta:
        managed = False
        db_table = 'sindicatospatronais'
        unique_together = (('registro', 'sind_empr', 'sind_fili', 'sind_codi'),)
