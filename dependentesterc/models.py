from django.db import models
from django.db import connection
from core.consultas import BancoConsulta


class Dependentesterc(models.Model):
    registro = models.CharField(max_length=14, primary_key=True)
    depe_empr = models.IntegerField()
    depe_fili = models.IntegerField()
    depe_terc = models.IntegerField()
    depe_codi = models.IntegerField()

    # ABA CADASTRADOS (1:1 tela legada Cadastro dependentes terceiros)
    depe_nome = models.CharField(max_length=200, blank=True, null=True)
    depe_nascimento = models.DateField(blank=True, null=True)
    depe_matricula = models.CharField(max_length=30, blank=True, null=True)
    depe_local_nascimento = models.CharField(max_length=60, blank=True, null=True)
    depe_cidade_codigo = models.IntegerField(blank=True, null=True)
    depe_cidade = models.CharField(max_length=60, blank=True, null=True)
    depe_cartorio = models.CharField(max_length=120, blank=True, null=True)
    depe_numero_registro = models.CharField(max_length=20, blank=True, null=True)
    depe_numero_livro = models.CharField(max_length=20, blank=True, null=True)
    depe_numero_folha = models.CharField(max_length=20, blank=True, null=True)
    depe_data_entrega = models.DateField(blank=True, null=True)
    depe_cpf = models.CharField(max_length=14, blank=True, null=True)
    depe_data_baixa = models.DateField(blank=True, null=True)
    depe_ir_ate = models.CharField(max_length=7, blank=True, null=True)  # Formato MM/AAAA
    depe_tipo_dependente = models.IntegerField(blank=True, null=True)
    depe_tipo_dependente_desc = models.CharField(max_length=60, blank=True, null=True)
    depe_descricao_dependencia = models.CharField(max_length=255, blank=True, null=True)
    depe_tipo_dependencia = models.IntegerField(blank=True, null=True)
    depe_invalido = models.BooleanField(default=False, blank=True, null=True)

    # ABA OBSERVACOES
    depe_observacoes = models.TextField(blank=True, null=True)

    objects = BancoConsulta()

    class Meta:
        managed = False
        db_table = "dependentesterc"
        unique_together = (
            ("registro", "depe_empr", "depe_fili", "depe_terc", "depe_codi"),
        )

    def __str__(self):
        return self.depe_nome or f"Dependente #{self.depe_codi}"

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
        using = kwargs.get("using") or self._state.db or "default"
        conn = self._get_connection(using)

        reg = str(getattr(self, "registro", None) or "")[:14]
        emp = int(self.depe_empr) if str(self.depe_empr or "").isdigit() else None
        fil = int(self.depe_fili) if str(self.depe_fili or "").isdigit() else None
        ter = int(self.depe_terc) if str(self.depe_terc or "").isdigit() else None
        cod = int(self.depe_codi) if str(self.depe_codi or "").isdigit() else None

        # --- (1) Verifica EXISTENCIA PK COMPOSTA 5 cols com RAW SQL ---
        pk_exists = False
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM dependentesterc WHERE registro = %s AND depe_empr = %s AND depe_fili = %s AND depe_terc = %s AND depe_codi = %s LIMIT 1",
                    [reg, emp, fil, ter, cod],
                )
                pk_exists = bool(cur.fetchone())
        except Exception:
            try:
                qs = Dependentesterc.objects.using(using).filter(
                    registro=reg, depe_empr=emp, depe_fili=fil,
                    depe_terc=ter, depe_codi=cod,
                )
                pk_exists = qs.exists()
            except Exception:
                pass

        # --- Coleta campos e valores por attname ---
        pk_field_names = {"registro", "depe_empr", "depe_fili", "depe_terc", "depe_codi"}
        ordered_fields = []
        field_values = {}
        for field in self._meta.local_concrete_fields:
            ordered_fields.append(field)
            field_values[field.attname] = getattr(self, field.attname)

        if pk_exists:
            # --- (2) UPDATE RAW SQL ---
            set_clause_parts = []
            params_update = []
            for field in ordered_fields:
                if field.attname in pk_field_names:
                    continue
                set_clause_parts.append(f'"{field.column}" = %s')
                params_update.append(field_values[field.attname])
            params_update.extend([reg, emp, fil, ter, cod])
            sql_up = (
                'UPDATE dependentesterc SET ' + ', '.join(set_clause_parts)
                + ' WHERE "registro"=%s AND "depe_empr"=%s AND "depe_fili"=%s AND "depe_terc"=%s AND "depe_codi"=%s'
            )
            with conn.cursor() as cur:
                cur.execute(sql_up, params_update)
            return self

        # --- (3) INSERT RAW SQL (FORCADO, SEM passar pelo super.save do Django) ---
        cols = []
        placeholders = []
        params_insert = []
        for field in ordered_fields:
            cols.append(f'"{field.column}"')
            placeholders.append("%s")
            params_insert.append(field_values[field.attname])
        sql_ins = 'INSERT INTO dependentesterc (' + ', '.join(cols) + ') VALUES (' + ', '.join(placeholders) + ')'
        with conn.cursor() as cur:
            cur.execute(sql_ins, params_insert)
        return self

    def delete(self, *args, **kwargs):
        using = kwargs.get("using") or self._state.db or "default"
        conn = self._get_connection(using)
        reg = str(getattr(self, "registro", None) or "")[:14]
        emp = int(self.depe_empr) if str(self.depe_empr or "").isdigit() else None
        fil = int(self.depe_fili) if str(self.depe_fili or "").isdigit() else None
        ter = int(self.depe_terc) if str(self.depe_terc or "").isdigit() else None
        cod = int(self.depe_codi) if str(self.depe_codi or "").isdigit() else None
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM dependentesterc WHERE "registro"=%s AND "depe_empr"=%s AND "depe_fili"=%s AND "depe_terc"=%s AND "depe_codi"=%s',
                [reg, emp, fil, ter, cod],
            )
