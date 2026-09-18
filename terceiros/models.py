from django.db import models
from django.db import connection

from core.consultas import BancoConsulta


class Terceiros(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)

    terc_empr = models.IntegerField(blank=True, null=True)
    terc_fili = models.IntegerField(blank=True, null=True)
    terc_codi = models.IntegerField(blank=True, null=True)

    terc_nome = models.CharField(max_length=200, blank=True, null=True)

    terc_inativo = models.BooleanField(blank=True, null=True)
    terc_cpf = models.CharField(max_length=14, blank=True, null=True)
    terc_cep = models.CharField(max_length=8, blank=True, null=True)
    terc_logr = models.IntegerField(blank=True, null=True)
    terc_ende = models.CharField(max_length=120, blank=True, null=True)
    terc_ende_nume = models.CharField(max_length=20, blank=True, null=True)
    terc_ende_comp = models.CharField(max_length=60, blank=True, null=True)
    terc_ende_bair = models.CharField(max_length=60, blank=True, null=True)
    terc_ende_cida_codi = models.IntegerField(blank=True, null=True)
    terc_ende_cida_desc = models.CharField(max_length=60, blank=True, null=True)
    terc_ende_uf = models.CharField(max_length=2, blank=True, null=True)
    terc_ddd = models.CharField(max_length=4, blank=True, null=True)
    terc_telefone = models.CharField(max_length=20, blank=True, null=True)
    terc_ddd_celular = models.CharField(max_length=4, blank=True, null=True)
    terc_celular = models.CharField(max_length=20, blank=True, null=True)
    terc_email = models.CharField(max_length=200, blank=True, null=True)

    terc_tipo_sanguineo = models.CharField(max_length=5, blank=True, null=True)
    terc_etnia_raca = models.IntegerField(blank=True, null=True)
    terc_cor_cabelo = models.IntegerField(blank=True, null=True)
    terc_cor_olhos = models.IntegerField(blank=True, null=True)
    terc_pessoa_com_deficiencia = models.BooleanField(blank=True, null=True)
    terc_observacoes_deficiencias = models.TextField(blank=True, null=True)
    terc_altura_metros = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    terc_peso_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    terc_sinais_no_corpo = models.BooleanField(blank=True, null=True)

    terc_nascimento = models.DateField(blank=True, null=True)
    terc_cidade_nascimento_codi = models.IntegerField(blank=True, null=True)
    terc_cidade_nascimento_desc = models.CharField(max_length=60, blank=True, null=True)
    terc_naturalidade = models.CharField(max_length=2, blank=True, null=True)
    terc_nome_mae = models.CharField(max_length=200, blank=True, null=True)
    terc_grau_instrucao = models.IntegerField(blank=True, null=True)
    terc_sexo = models.IntegerField(blank=True, null=True)
    terc_estado_civil = models.IntegerField(blank=True, null=True)
    terc_controlar_manual_dependentes_ir = models.BooleanField(blank=True, null=True)
    terc_numero_dependentes_ir = models.IntegerField(blank=True, null=True, default=0)

    terc_pais_nacionalidade_codi = models.IntegerField(blank=True, null=True)
    terc_pais_nacionalidade_desc = models.CharField(max_length=80, blank=True, null=True)
    terc_chegada_brasil = models.DateField(blank=True, null=True)
    terc_casado_brasileiro = models.BooleanField(blank=True, null=True)
    terc_tem_filhos_brasileiros = models.BooleanField(blank=True, null=True)
    terc_rne = models.CharField(max_length=20, blank=True, null=True)
    terc_orgao_uf_emissao_rne = models.CharField(max_length=30, blank=True, null=True)
    terc_emissao_rne = models.DateField(blank=True, null=True)
    terc_tempo_residencia = models.IntegerField(blank=True, null=True)
    terc_condicao_ingresso = models.IntegerField(blank=True, null=True)
    terc_pais_residencia_codi = models.IntegerField(blank=True, null=True)
    terc_pais_residencia_desc = models.CharField(max_length=80, blank=True, null=True)
    terc_residencia_exterior = models.BooleanField(blank=True, null=True)
    terc_ende_exterior = models.CharField(max_length=120, blank=True, null=True)
    terc_ende_exterior_nume = models.CharField(max_length=20, blank=True, null=True)
    terc_ende_exterior_comp = models.CharField(max_length=60, blank=True, null=True)
    terc_ende_exterior_bair = models.CharField(max_length=60, blank=True, null=True)
    terc_ende_exterior_cidade = models.CharField(max_length=60, blank=True, null=True)
    terc_ende_exterior_codigo_postal = models.CharField(max_length=20, blank=True, null=True)

    terc_banco = models.IntegerField(blank=True, null=True)
    terc_banco_desc = models.CharField(max_length=120, blank=True, null=True)
    terc_conta_corrente = models.CharField(max_length=20, blank=True, null=True)
    terc_digito_conta_corrente = models.CharField(max_length=5, blank=True, null=True)
    terc_tipo_conta = models.IntegerField(blank=True, null=True)
    terc_modo_pagamento = models.IntegerField(blank=True, null=True)
    terc_rg = models.CharField(max_length=20, blank=True, null=True)
    terc_orgao_emissor_rg = models.CharField(max_length=20, blank=True, null=True)
    terc_emissao_rg = models.DateField(blank=True, null=True)
    terc_uf_rg = models.CharField(max_length=2, blank=True, null=True)
    terc_certificado_reservista = models.CharField(max_length=30, blank=True, null=True)
    terc_titulo_eleitor = models.CharField(max_length=20, blank=True, null=True)
    terc_zona_titulo = models.CharField(max_length=5, blank=True, null=True)
    terc_secao_titulo = models.CharField(max_length=5, blank=True, null=True)
    terc_conselho_regional_numero = models.CharField(max_length=30, blank=True, null=True)
    terc_conselho_regional_sigla = models.CharField(max_length=20, blank=True, null=True)
    terc_ctps_numero = models.CharField(max_length=20, blank=True, null=True)
    terc_ctps_serie = models.CharField(max_length=10, blank=True, null=True)
    terc_ctps_digito = models.CharField(max_length=2, blank=True, null=True)
    terc_ctps_data = models.DateField(blank=True, null=True)
    terc_ctps_uf = models.CharField(max_length=2, blank=True, null=True)
    terc_carne_inss_numero = models.CharField(max_length=20, blank=True, null=True)
    terc_codigo_ccm = models.CharField(max_length=20, blank=True, null=True)
    terc_carteira_identidade_arquivo = models.BinaryField(blank=True, null=True)

    terc_classe = models.IntegerField(blank=True, null=True)
    terc_classe_desc = models.CharField(max_length=120, blank=True, null=True)
    terc_cbo = models.IntegerField(blank=True, null=True)
    terc_cbo_desc = models.CharField(max_length=160, blank=True, null=True)
    terc_natureza_ocupacao = models.IntegerField(blank=True, null=True)
    terc_categoria_sefip = models.IntegerField(blank=True, null=True)
    terc_categoria_esocial = models.IntegerField(blank=True, null=True)
    terc_grau_risco = models.IntegerField(blank=True, null=True)
    terc_transportador_autonomo_perc_inss = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    terc_percentual_contr_ir = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    terc_descontar_iss = models.BooleanField(blank=True, null=True, default=False)
    terc_percentual_iss = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    terc_tributacao_irrf_exterior = models.IntegerField(blank=True, null=True)
    terc_tributacao_irrf_exterior_desc = models.CharField(max_length=80, blank=True, null=True)
    terc_rat_aposentadoria_perc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    terc_acordo_internacional_inss = models.BooleanField(blank=True, null=True)
    terc_percentual_irrf_exterior = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    terc_nif = models.CharField(max_length=30, blank=True, null=True)
    terc_beneficiario_dispensado_nif = models.BooleanField(blank=True, null=True)
    terc_pais_nao_exige_nif = models.BooleanField(blank=True, null=True)
    terc_cartao_ponto = models.IntegerField(blank=True, null=True)

    terc_data_admissao = models.DateField(blank=True, null=True)

    objects = BancoConsulta()

    def __str__(self):
        return self.terc_nome or f"Terceiro #{self.terc_codi}"

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

        empr = getattr(self, "terc_empr", None)
        fili = getattr(self, "terc_fili", None)
        codi = getattr(self, "terc_codi", None)
        reg = getattr(self, "registro", None)

        # --- (1) Verifica se JA EXISTE essa PK COMPOSTA no banco ---
        pk_exists = False
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM terceiros WHERE registro = %s AND terc_empr = %s AND terc_fili = %s AND terc_codi = %s LIMIT 1",
                    [
                        str(reg or "")[:14],
                        int(empr) if str(empr or "").isdigit() else None,
                        int(fili) if str(fili or "").isdigit() else None,
                        int(codi) if str(codi or "").isdigit() else None,
                    ],
                )
                pk_exists = bool(cur.fetchone())
        except Exception:
            # Fallback se a consulta bruta falhar: usa ORM filter
            qs = self.__class__.objects.using(using or "default").filter(
                registro=self.registro, terc_empr=self.terc_empr,
                terc_fili=self.terc_fili, terc_codi=self.terc_codi,
            )
            pk_exists = qs.exists()

        # --- PROTECAO NUCLEAR ANTI-SOBRESCRITA:
        #     Se MODO CRIAR (view Novo Terceiro) e JA EXISTE a PK no banco:
        #     ☢️ NAO DEIXA GRAVAR DE JEITO NENHUM! Levanta exception!
        if operacao == "criar" and pk_exists:
            raise RuntimeError(
                "[PROTECAO SOBRESCRITA ATIVADA]: Tentativa de INSERT duplicado em Terceiros "
                f"com PK (registro={reg!r}, empr={empr}, fili={fili}, cod={codi}) que JA EXISTE no banco! "
                "Nao foi permitido sobrescrever o cadastro existente. Contate o suporte."
            )

        # --- Coleta TODOS os valores dos campos com attname ---
        field_values = {}
        pk_field_names = {"registro", "terc_empr", "terc_fili", "terc_codi"}
        ordered_fields = []
        for field in self._meta.local_concrete_fields:
            ordered_fields.append(field)
            field_values[field.attname] = getattr(self, field.attname)

        # --- (2) JA EXISTE? FAZ UPDATE VIA RAW SQL ---
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
                'UPDATE terceiros SET ' + ', '.join(set_clause_parts)
                + ' WHERE "registro" = %s AND "terc_empr" = %s AND "terc_fili" = %s AND "terc_codi" = %s'
            )
            with conn.cursor() as cur:
                cur.execute(sql_update, params_update)
            return self

        # --- (3) NAO EXISTE? FAZ INSERT VIA RAW SQL (FORCA INSERT MESMO SE instance.pk NAO For None) ---
        cols = []
        placeholders = []
        params_insert = []
        for field in ordered_fields:
            cols.append(f'"{field.column}"')
            placeholders.append("%s")
            params_insert.append(field_values[field.attname])
        sql_insert = 'INSERT INTO terceiros (' + ', '.join(cols) + ') VALUES (' + ', '.join(placeholders) + ')'
        with conn.cursor() as cur:
            cur.execute(sql_insert, params_insert)
        return self

    def delete(self, *args, **kwargs):
        using = kwargs.get("using") or self._state.db
        try:
            from dependentesterc.models import Dependentesterc

            Dependentesterc.objects.using(using).filter(
                registro=self.registro,
                depe_empr=self.terc_empr,
                depe_fili=self.terc_fili,
                depe_terc=self.terc_codi,
            ).delete()
        except Exception:
            pass
        conn = self._get_connection(using)
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM terceiros WHERE "registro" = %s AND "terc_empr" = %s AND "terc_fili" = %s AND "terc_codi" = %s',
                [
                    str(getattr(self, "registro", None) or "")[:14],
                    int(getattr(self, "terc_empr")) if str(getattr(self, "terc_empr") or "").isdigit() else None,
                    int(getattr(self, "terc_fili")) if str(getattr(self, "terc_fili") or "").isdigit() else None,
                    int(getattr(self, "terc_codi")) if str(getattr(self, "terc_codi") or "").isdigit() else None,
                ],
            )

    class Meta:
        managed = False
        db_table = 'terceiros'
        unique_together = (('registro','terc_empr','terc_fili','terc_codi'),)
