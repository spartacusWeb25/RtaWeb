from django.db import models
from django.db import connection
from django.db import connections


class DepartamentosRh(models.Model):
    # ============================================================
    # PK COMPOSTA REAL 4 colunas (igual todos os outros apps)
    # ============================================================
    registro = models.CharField(primary_key=True, max_length=14)
    depa_empr = models.IntegerField(blank=True, null=True)
    depa_fili = models.IntegerField(blank=True, null=True)
    depa_codi = models.IntegerField(blank=True, null=True)

    # ============================================================
    # ABA 1: CADASTRAIS (básicos + endereço + contato + doc + tomador)
    # ============================================================
    depa_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descrição")
    depa_apelido = models.CharField(max_length=100, blank=True, null=True, verbose_name="Apelido")

    # --- Endereço ---
    depa_cep = models.CharField(max_length=8, blank=True, null=True, verbose_name="CEP")
    depa_logr = models.IntegerField(blank=True, null=True, verbose_name="Logradouro (código)")
    depa_logr_desc = models.CharField(max_length=80, blank=True, null=True, verbose_name="Logradouro descrição")
    depa_ende = models.CharField(max_length=160, blank=True, null=True, verbose_name="Endereço")
    depa_ende_nume = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número")
    depa_ende_comp = models.CharField(max_length=80, blank=True, null=True, verbose_name="Complemento")
    depa_ende_bair = models.CharField(max_length=80, blank=True, null=True, verbose_name="Bairro")
    depa_cida_codi = models.IntegerField(blank=True, null=True, verbose_name="Cidade (código)")
    depa_cida_desc = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade descrição")
    depa_esta = models.CharField(max_length=2, blank=True, null=True, verbose_name="UF")

    # --- Contato ---
    depa_ddd1 = models.CharField(max_length=4, blank=True, null=True, verbose_name="DDD")
    depa_fone1 = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    depa_emai = models.CharField(max_length=120, blank=True, null=True, verbose_name="E-mail")

    # --- Documento / Tomador (eSocial) ---
    # depa_tipo_doc: 1 = CNPJ, 2 = CEI
    depa_tipo_doc = models.IntegerField(blank=True, null=True, default=1, verbose_name="Tipo do documento (1=CNPJ / 2=CEI)")
    depa_cnpj = models.CharField(max_length=14, blank=True, null=True, verbose_name="CNPJ / CEI")
    depa_tipo_tomador = models.IntegerField(blank=True, null=True, verbose_name="Tipo tomador (código eSocial)")
    depa_tipo_tomador_desc = models.CharField(max_length=160, blank=True, null=True,
                                              verbose_name="Tipo tomador descrição")

    depa_inativo = models.BooleanField(blank=True, null=True, default=False, verbose_name="Inativo")

    # ============================================================
    # ABA 2: INFORMAÇÕES MENSAIS (Terceiro / FPAS / CNAE / GPS / etc)
    # ============================================================
    # Terceiro
    depa_im_terc = models.IntegerField(blank=True, null=True, verbose_name="Terceiro (código)")
    depa_im_terc_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="Terceiro descrição")

    # FPAS
    depa_fpas_codi = models.IntegerField(blank=True, null=True, verbose_name="FPAS código")
    depa_fpas_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="FPAS descrição")
    depa_fpas_perc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="% FPAS")

    # CNAE / RAT 2.0
    depa_cnae_codi = models.IntegerField(blank=True, null=True, verbose_name="CNAE/RAT 2.0 código")
    depa_cnae_desc = models.CharField(max_length=250, blank=True, null=True, verbose_name="CNAE/RAT 2.0 descrição")
    depa_cnae_perc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="% CNAE")
    depa_fap_aliq = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True, verbose_name="Alíquota FAP")

    # Códigos GPS
    depa_gps_pag_codi = models.IntegerField(blank=True, null=True, verbose_name="Código pagamento GPS")
    depa_gps_pag_desc = models.CharField(max_length=220, blank=True, null=True,
                                         verbose_name="Código pagamento GPS descrição")
    depa_gps_transp_codi = models.IntegerField(blank=True, null=True, verbose_name="Código GPS transportador")
    depa_gps_transp_desc = models.CharField(max_length=220, blank=True, null=True,
                                            verbose_name="Código GPS transportador descrição")

    # Dados cadastrais / percentuais (opções: 1=Nenhum / 2=Empresa / 3=Filial / ...)
    depa_dados_cad_codi = models.IntegerField(blank=True, null=True, default=1,
                                              verbose_name="Dados cadastrais (1=Nenhum...)")
    depa_dados_perc_codi = models.IntegerField(blank=True, null=True, default=1,
                                               verbose_name="Dados percentuais (1=Nenhum...)")
    depa_tx_servico = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True,
                                          verbose_name="Taxa de serviço")
    depa_contab_codi = models.CharField(max_length=40, blank=True, null=True,
                                        verbose_name="Código na contabilidade")
    depa_mensagens1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mensagens linha 1")
    depa_mensagens2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mensagens linha 2")

    # ============================================================
    # LOGS (padrão projeto: usuário + data criar/editar)
    # ============================================================
    depa_usuario_inc = models.CharField(max_length=30, blank=True, null=True)
    depa_data_inc = models.DateTimeField(blank=True, null=True)
    depa_usuario_alt = models.CharField(max_length=30, blank=True, null=True)
    depa_data_alt = models.DateTimeField(blank=True, null=True)

    # ============================================================
    # Internos do model: conexão, save raw SQL, delete raw SQL
    # ============================================================
    def _get_connection(self, using=None):
        try:
            alias = using or "default"
            conn = connections[alias]
        except Exception:
            conn = connection
        return conn

    def save(self, *args, **kwargs):
        operacao = kwargs.pop("operacao", None)
        using = kwargs.get("using") or self._state.db
        conn = self._get_connection(using)

        empr = getattr(self, "depa_empr", None)
        fili = getattr(self, "depa_fili", None)
        codi = getattr(self, "depa_codi", None)
        reg = getattr(self, "registro", None)

        pk_exists = False
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM departamentosrh "
                    "WHERE registro = %s AND depa_empr = %s AND depa_fili = %s AND depa_codi = %s LIMIT 1",
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
                registro=self.registro, depa_empr=self.depa_empr,
                depa_fili=self.depa_fili, depa_codi=self.depa_codi,
            )
            pk_exists = qs.exists()

        if operacao == "criar" and pk_exists:
            raise RuntimeError(
                "[PROTECAO SOBRESCRITA ATIVADA]: Tentativa de INSERT duplicado em DepartamentosRh "
                f"com PK (registro={reg!r}, empr={empr}, fili={fili}, cod={codi}) que JA EXISTE no banco! "
                "Nao foi permitido sobrescrever o cadastro existente."
            )

        field_values = {}
        pk_field_names = {"registro", "depa_empr", "depa_fili", "depa_codi"}
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
                'UPDATE departamentosrh SET ' + ', '.join(set_clause_parts)
                + ' WHERE "registro" = %s AND "depa_empr" = %s AND "depa_fili" = %s AND "depa_codi" = %s'
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
        sql_insert = ('INSERT INTO departamentosrh (' + ', '.join(cols)
                      + ') VALUES (' + ', '.join(placeholders) + ')')
        with conn.cursor() as cur:
            cur.execute(sql_insert, params_insert)
        return self

    def delete(self, *args, **kwargs):
        using = kwargs.get("using") or self._state.db
        conn = self._get_connection(using)
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM departamentosrh '
                'WHERE "registro" = %s AND "depa_empr" = %s AND "depa_fili" = %s AND "depa_codi" = %s',
                [
                    str(getattr(self, "registro", None) or "")[:14],
                    int(getattr(self, "depa_empr")) if str(getattr(self, "depa_empr") or "").isdigit() else None,
                    int(getattr(self, "depa_fili")) if str(getattr(self, "depa_fili") or "").isdigit() else None,
                    int(getattr(self, "depa_codi")) if str(getattr(self, "depa_codi") or "").isdigit() else None,
                ],
            )

    class Meta:
        managed = False
        db_table = 'departamentosrh'
