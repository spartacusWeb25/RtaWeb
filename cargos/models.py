from django.db import models
from django.db import connection

from core.consultas import BancoConsulta


class Cargos(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    carg_empr = models.IntegerField(blank=True, null=True)
    carg_fili = models.IntegerField(blank=True, null=True)
    carg_codi = models.IntegerField(blank=True, null=True)

    carg_descricao = models.CharField(max_length=200, blank=True, null=True)
    carg_inativo = models.BooleanField(blank=True, null=True, default=False)
    carg_cbo_codi = models.IntegerField(blank=True, null=True)
    carg_cbo_desc = models.CharField(max_length=200, blank=True, null=True)

    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)

    objects = BancoConsulta()

    def __str__(self):
        return self.carg_descricao or f"Cargo #{self.carg_codi}"

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

        empr = getattr(self, "carg_empr", None)
        fili = getattr(self, "carg_fili", None)
        codi = getattr(self, "carg_codi", None)
        reg = getattr(self, "registro", None)

        pk_exists = False
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM cargos WHERE registro = %s AND carg_empr = %s AND carg_fili = %s AND carg_codi = %s LIMIT 1",
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
                registro=self.registro, carg_empr=self.carg_empr,
                carg_fili=self.carg_fili, carg_codi=self.carg_codi,
            )
            pk_exists = qs.exists()

        if operacao == "criar" and pk_exists:
            raise RuntimeError(
                "[PROTECAO SOBRESCRITA ATIVADA]: Tentativa de INSERT duplicado em Cargos "
                f"com PK (registro={reg!r}, empr={empr}, fili={fili}, cod={codi}) que JA EXISTE no banco! "
                "Nao foi permitido sobrescrever o cadastro existente. Contate o suporte."
            )

        field_values = {}
        pk_field_names = {"registro", "carg_empr", "carg_fili", "carg_codi"}
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
                'UPDATE cargos SET ' + ', '.join(set_clause_parts)
                + ' WHERE "registro" = %s AND "carg_empr" = %s AND "carg_fili" = %s AND "carg_codi" = %s'
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
        sql_insert = 'INSERT INTO cargos (' + ', '.join(cols) + ') VALUES (' + ', '.join(placeholders) + ')'
        with conn.cursor() as cur:
            cur.execute(sql_insert, params_insert)
        return self

    def delete(self, *args, **kwargs):
        using = kwargs.get("using") or self._state.db
        conn = self._get_connection(using)
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM cargos WHERE "registro" = %s AND "carg_empr" = %s AND "carg_fili" = %s AND "carg_codi" = %s',
                [
                    str(getattr(self, "registro", None) or "")[:14],
                    int(getattr(self, "carg_empr")) if str(getattr(self, "carg_empr") or "").isdigit() else None,
                    int(getattr(self, "carg_fili")) if str(getattr(self, "carg_fili") or "").isdigit() else None,
                    int(getattr(self, "carg_codi")) if str(getattr(self, "carg_codi") or "").isdigit() else None,
                ],
            )

    class Meta:
        managed = False
        db_table = 'cargos'
        unique_together = (('registro', 'carg_empr', 'carg_fili', 'carg_codi'),)
