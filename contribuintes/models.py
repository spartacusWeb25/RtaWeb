from django.db import models

from core.consultas import BancoConsulta


class Contribuintes(models.Model):
    # Mantemos `registro` como chave tecnica do ORM para evitar um `id`
    # automatico do Django. A PK REAL no Postgres e a composta
    # (registro, contr_empr, contr_codi, contr_fili).
    registro = models.CharField(primary_key=True, max_length=14)

    # =========================================================
    # CHAVE COMPOSTA (4 campos)
    # =========================================================
    contr_empr = models.IntegerField(blank=True, null=True)
    contr_fili = models.IntegerField(blank=True, null=True)
    contr_codi = models.IntegerField(blank=True, null=True)

    # =========================================================
    # ABA 1 — CADASTRAS
    # =========================================================
    contr_admissao_preliminar = models.IntegerField(blank=True, null=True)
    contr_nome = models.CharField(max_length=200, blank=True, null=True)
    contr_email = models.CharField(max_length=200, blank=True, null=True)
    contr_matricula_esocial = models.CharField(max_length=30, blank=True, null=True)

    contr_cep = models.CharField(max_length=8, blank=True, null=True)
    contr_logr = models.IntegerField(blank=True, null=True)
    contr_ende = models.CharField(max_length=120, blank=True, null=True)
    contr_ende_nume = models.CharField(max_length=20, blank=True, null=True)
    contr_ende_comp = models.CharField(max_length=60, blank=True, null=True)
    contr_ende_bair = models.CharField(max_length=60, blank=True, null=True)
    contr_ende_cida_codi = models.IntegerField(blank=True, null=True)
    contr_ende_cida_desc = models.CharField(max_length=60, blank=True, null=True)
    contr_ende_uf = models.CharField(max_length=2, blank=True, null=True)
    contr_ddd = models.CharField(max_length=4, blank=True, null=True)
    contr_telefone = models.CharField(max_length=20, blank=True, null=True)
    contr_ddd_celular = models.CharField(max_length=4, blank=True, null=True)
    contr_celular = models.CharField(max_length=20, blank=True, null=True)

    contr_residencia_exterior = models.BooleanField(blank=True, null=True)
    contr_pais_residencia_codi = models.IntegerField(blank=True, null=True)
    contr_pais_residencia_desc = models.CharField(max_length=80, blank=True, null=True)
    contr_ende_exterior = models.CharField(max_length=120, blank=True, null=True)
    contr_ende_exterior_nume = models.CharField(max_length=20, blank=True, null=True)
    contr_ende_exterior_comp = models.CharField(max_length=60, blank=True, null=True)
    contr_ende_exterior_bair = models.CharField(max_length=60, blank=True, null=True)
    contr_ende_exterior_cidade = models.CharField(max_length=60, blank=True, null=True)
    contr_ende_exterior_codigo_postal = models.CharField(max_length=20, blank=True, null=True)

    # =========================================================
    # ABA 2 — FÍSICO
    # =========================================================
    contr_tipo_sanguineo = models.CharField(max_length=5, blank=True, null=True)
    contr_etnia_raca = models.IntegerField(blank=True, null=True)
    contr_sexo = models.IntegerField(blank=True, null=True)
    # ------------- db_column (legado: "deficiencia" = "pessoa com deficiencia")
    contr_pessoa_com_deficiencia = models.BooleanField(
        blank=True, null=True, db_column="contr_deficiencia"
    )
    contr_deficiencia_fisica = models.BooleanField(blank=True, null=True)
    contr_deficiencia_auditiva = models.BooleanField(blank=True, null=True)
    contr_deficiencia_visual = models.BooleanField(blank=True, null=True)
    contr_deficiencia_intelectual = models.BooleanField(blank=True, null=True)
    contr_deficiencia_mental = models.BooleanField(blank=True, null=True)
    contr_reabilitado = models.BooleanField(blank=True, null=True)
    contr_foto_3x4 = models.BinaryField(blank=True, null=True)
    contr_observacoes_deficiencias = models.TextField(blank=True, null=True)

    # =========================================================
    # ABA 3 — HISTÓRICO
    # =========================================================
    contr_pais_nascimento_codi = models.IntegerField(blank=True, null=True)
    contr_pais_nascimento_desc = models.CharField(max_length=80, blank=True, null=True)
    contr_cidade_nascimento_codi = models.IntegerField(blank=True, null=True)
    contr_cidade_nascimento_desc = models.CharField(max_length=60, blank=True, null=True)
    contr_naturalidade = models.CharField(max_length=2, blank=True, null=True)
    contr_nascimento = models.DateField(blank=True, null=True)
    contr_estado_civil = models.IntegerField(blank=True, null=True)
    contr_grau_instrucao = models.IntegerField(blank=True, null=True)

    # -------- db_columns (datas historico legado)
    contr_admissao = models.DateField(
        blank=True, null=True, db_column="contr_data_entrada"
    )
    contr_cadastro = models.DateField(
        blank=True, null=True, db_column="contr_data_cadastro"
    )
    contr_inicio_adicional_tempo_servico = models.DateField(blank=True, null=True)
    contr_data_saida = models.DateField(
        blank=True, null=True, db_column="contr_data_baixa"
    )
    contr_data_pagamento_baixa = models.DateField(blank=True, null=True)
    contr_motivo_desligamento = models.IntegerField(blank=True, null=True)
    contr_esocial_indicativo_pensao_alimenticia_fgts = models.IntegerField(blank=True, null=True)
    contr_pensao_fgts_valor = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    contr_pensao_fgts_percentual = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    # =========================================================
    # ABA 4 — ESTRANGEIRO (campos que existem no banco, adicionados)
    # =========================================================
    contr_pais_nacionalidade_codi = models.IntegerField(blank=True, null=True)
    contr_pais_nacionalidade_desc = models.CharField(max_length=80, blank=True, null=True)
    contr_chegada_brasil = models.DateField(blank=True, null=True)
    contr_casado_brasileiro = models.BooleanField(blank=True, null=True)
    contr_tem_filhos_brasileiros = models.BooleanField(blank=True, null=True)
    contr_rne = models.CharField(max_length=20, blank=True, null=True)
    contr_orgao_uf_emissao_rne = models.CharField(max_length=30, blank=True, null=True)
    contr_emissao_rne = models.DateField(blank=True, null=True)
    contr_tempo_residencia = models.IntegerField(blank=True, null=True)
    contr_condicao_ingresso = models.IntegerField(blank=True, null=True)

    # =========================================================
    # ABA 5 — DOCUMENTOS
    # =========================================================
    contr_cpf = models.CharField(max_length=14, blank=True, null=True)
    contr_nis = models.CharField(max_length=14, blank=True, null=True)
    contr_emissao_nis = models.DateField(blank=True, null=True)
    contr_rg = models.CharField(max_length=20, blank=True, null=True)
    contr_orgao_emissor_rg = models.CharField(max_length=20, blank=True, null=True)
    contr_uf_rg = models.CharField(max_length=2, blank=True, null=True)
    contr_emissao_rg = models.DateField(blank=True, null=True)
    contr_carteira_trabalho = models.CharField(max_length=20, blank=True, null=True)
    contr_serie_carteira_trabalho = models.CharField(max_length=10, blank=True, null=True)
    contr_digito_serie_carteira_trabalho = models.CharField(max_length=2, blank=True, null=True)
    contr_uf_carteira_trabalho = models.CharField(max_length=2, blank=True, null=True)
    contr_emissao_carteira_trabalho = models.DateField(blank=True, null=True)
    contr_cnh = models.CharField(max_length=20, blank=True, null=True)
    contr_categoria_cnh = models.CharField(max_length=5, blank=True, null=True)
    contr_uf_cnh = models.CharField(max_length=2, blank=True, null=True)
    contr_emissao_cnh = models.DateField(blank=True, null=True)
    contr_vencimento_cnh = models.DateField(blank=True, null=True)
    contr_primeira_habilitacao = models.DateField(blank=True, null=True)
    contr_titulo_eleitor = models.CharField(max_length=20, blank=True, null=True)

    # -------- db_columns (legado: zona/secao + "titulo_eleitor")
    contr_zona_titulo = models.CharField(
        max_length=5, blank=True, null=True, db_column="contr_zona_titulo_eleitor"
    )
    contr_secao_titulo = models.CharField(
        max_length=5, blank=True, null=True, db_column="contr_secao_titulo_eleitor"
    )
    contr_certificado_reservista = models.CharField(max_length=30, blank=True, null=True)
    contr_carteira_identidade_arquivo = models.BinaryField(blank=True, null=True)
    contr_aviso_carteira_trabalho_digital = models.BooleanField(
        blank=True, null=True, default=True
    )

    # =========================================================
    # ABA 6 — DEPENDENTES (campos no contribuinte)
    # =========================================================
    contr_nome_pai = models.CharField(max_length=200, blank=True, null=True)
    contr_nome_mae = models.CharField(max_length=200, blank=True, null=True)
    contr_tem_dependentes = models.BooleanField(blank=True, null=True, default=False)

    # =========================================================
    # ABA 7 — FGTS/GPS
    # =========================================================
    contr_categoria_sefip = models.IntegerField(blank=True, null=True)
    contr_categoria_esocial = models.IntegerField(blank=True, null=True)
    contr_categoria_esocial_desc = models.CharField(max_length=120, blank=True, null=True)
    contr_transp_autonomo_contribuicao_inss = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    contr_percentual_contr_ir = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    contr_data_opcao = models.DateField(blank=True, null=True)
    contr_percentual_fgts = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    contr_grau_risco = models.IntegerField(blank=True, null=True)
    contr_rat_aposentadoria = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    contr_descontar_iss = models.BooleanField(blank=True, null=True)
    contr_percentual_iss = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    contr_regime_previdenciario = models.IntegerField(blank=True, null=True)
    contr_categoria_origem = models.IntegerField(blank=True, null=True)
    contr_tipo_cnpj_cpf_origem = models.IntegerField(blank=True, null=True)
    contr_cnpj_cpf_origem = models.CharField(max_length=14, blank=True, null=True)
    contr_admissao_origem = models.DateField(blank=True, null=True)
    contr_matricula_origem = models.CharField(max_length=30, blank=True, null=True)
    contr_regime_previdenciario_origem = models.IntegerField(blank=True, null=True)

    # =========================================================
    # ABA 8 — VÍNCULOS
    # =========================================================
    contr_classe = models.IntegerField(blank=True, null=True)
    contr_vinculo_empregaticio = models.IntegerField(blank=True, null=True)
    contr_vinculo_empregaticio_desc = models.CharField(max_length=120, blank=True, null=True)
    contr_depto = models.IntegerField(blank=True, null=True)
    contr_depto_desc = models.CharField(max_length=120, blank=True, null=True)
    contr_ccusto = models.IntegerField(blank=True, null=True)
    contr_ccusto_desc = models.CharField(max_length=120, blank=True, null=True)
    contr_cargo = models.IntegerField(blank=True, null=True)
    contr_cargo_desc = models.CharField(max_length=120, blank=True, null=True)
    contr_cbo = models.CharField(max_length=10, blank=True, null=True)
    contr_cbo_desc = models.CharField(max_length=120, blank=True, null=True)
    contr_natureza_ocupacao = models.IntegerField(blank=True, null=True)
    contr_orgao_classe = models.BooleanField(blank=True, null=True)
    contr_inscricao_orgao_classe = models.CharField(max_length=30, blank=True, null=True)
    contr_orgao_uf_emissao_orgao_classe = models.CharField(max_length=30, blank=True, null=True)
    contr_emissao_orgao_classe = models.DateField(blank=True, null=True)
    contr_validade_orgao_classe = models.DateField(blank=True, null=True)

    # =========================================================
    # ABA 9 — CÁLCULO
    # =========================================================
    contr_forma_pagamento = models.IntegerField(blank=True, null=True)
    contr_remuneracao = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    contr_nao_arredondar = models.BooleanField(blank=True, null=True)
    contr_descontar_inss_do_ir = models.BooleanField(blank=True, null=True)
    contr_adiantamento = models.BooleanField(blank=True, null=True)
    contr_valor_previdencia_privada = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    contr_valor_previdencia_privada_13 = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    contr_aplica_deducao_mais_benefica_irrf = models.BooleanField(blank=True, null=True)
    contr_base_inss_multiplos_vinculos = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    contr_valor_inss_multiplos_vinculos = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    contr_base_ir_multiplos_vinculos = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    contr_valor_ir_multiplos_vinculos = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    contr_base_inss_multiplos_vinculos_13 = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    contr_valor_inss_multiplos_vinculos_13 = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    contr_base_ir_multiplos_vinculos_13 = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    contr_valor_ir_multiplos_vinculos_13 = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )

    # =========================================================
    # ABA 10 — BANCO
    # =========================================================
    contr_banco = models.IntegerField(blank=True, null=True)
    contr_banco_desc = models.CharField(max_length=120, blank=True, null=True)
    contr_conta_corrente = models.CharField(max_length=20, blank=True, null=True)
    contr_digito_conta_corrente = models.CharField(max_length=5, blank=True, null=True)
    contr_tipo_conta = models.IntegerField(blank=True, null=True)
    contr_modo_pagamento = models.IntegerField(blank=True, null=True)

    # =========================================================
    # ABA 11 — eSocial (Qualificação + Integração)
    # =========================================================
    contr_esocial_qualif_status = models.CharField(max_length=500, blank=True, null=True)
    contr_esocial_qualif_mensagem = models.TextField(blank=True, null=True)
    contr_esocial_qualif_data_hora = models.DateTimeField(blank=True, null=True)
    contr_esocial_integrado = models.BooleanField(blank=True, null=True, default=False)
    contr_esocial_integra_data_hora = models.DateTimeField(blank=True, null=True)
    contr_esocial_integra_numero_recibo = models.CharField(max_length=80, blank=True, null=True)

    # =========================================================
    # ABA 12 — OBSERVAÇÕES e Inativo
    # =========================================================
    contr_observacoes = models.TextField(blank=True, null=True)
    contr_inativo = models.BooleanField(blank=True, null=True)

    # =========================================================
    # BancoConsulta manager (multi-tenant .using(db_alias))
    # =========================================================
    objects = BancoConsulta()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_chave_composta = self._get_chave_composta()

    def _get_chave_composta(self):
        return {
            "registro": self.registro,
            "contr_empr": self.contr_empr,
            "contr_codi": self.contr_codi,
            "contr_fili": self.contr_fili,
        }

    def save(self, *args, **kwargs):
        using = kwargs.get("using") or self._state.db

        if self._state.adding:
            if using:
                kwargs["using"] = using
            kwargs["force_insert"] = True
            result = super().save(*args, **kwargs)
            self._original_chave_composta = self._get_chave_composta()
            return result

        valores = {
            field.attname: getattr(self, field.attname)
            for field in self._meta.local_concrete_fields
        }
        updated = self.__class__.objects.using(using).filter(
            **self._original_chave_composta
        ).update(**valores)
        if not updated:
            raise self.__class__.DoesNotExist(
                "Contribuinte nao encontrado para atualizacao."
            )

        self._original_chave_composta = self._get_chave_composta()

    def delete(self, using=None, keep_parents=False):
        using = using or self._state.db
        try:
            from dependentescontr.models import Dependentescontr

            registro = getattr(self, "registro", None)
            empr = getattr(self, "contr_empr", None)
            fili = getattr(self, "contr_fili", None)
            contr = getattr(self, "contr_codi", None)
            if registro and empr is not None and fili is not None and contr is not None:
                try:
                    qs_dep = Dependentescontr.objects
                    if using:
                        qs_dep = qs_dep.using(using)
                    qs_dep.filter(
                        registro=registro,
                        depecontr_empr=int(empr),
                        depecontr_fili=int(fili),
                        depecontr_contr=int(contr),
                    ).delete()
                except Exception:
                    pass
        except Exception:
            pass
        deleted_count, _ = (
            self.__class__.objects.using(using)
            .filter(**self._get_chave_composta())
            .delete()
        )
        return deleted_count, {}

    class Meta:
        managed = False
        db_table = "contribuintes"
        unique_together = (("registro", "contr_empr", "contr_codi", "contr_fili"),)
