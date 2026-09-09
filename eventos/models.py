from django.db import models
from core.consultas import BancoConsulta
from eventos.web.choices import (
    TIPO_REFERENCIA_CHOICES,
    TIPO_VERBA_CHOICES,
    NATUREZA_RUBRICA_CHOICES,
    TETO_REMUNERATORIO_CHOICES,
    INCIDENCIA_CPRP_CHOICES,
    FUNCIONARIOS_AFASTADOS_CHOICES,
)


class Eventos(models.Model):
    """
    Cadastro de Verbas / Eventos de Folha.

    Estrutura baseada nos prints do sistema legado, organizada em 3 abas:
      1. Incidência
      2. Características
      3. Fórmulas

    Chave primária composta REAL no banco:  (registro, even_empr, even_codi)
    Todos os demais campos possuem prefixo even_ (padrão legado).
    """

    # ------------------------------------------------------------------
    # 🔑 CHAVE COMPOSTA (não renomear estes 3 campos)
    # ------------------------------------------------------------------
    registro = models.CharField(primary_key=True, max_length=14)
    even_empr = models.IntegerField()
    even_codi = models.IntegerField()

    # ==================================================================
    # 🧾 CABEÇALHO (exibido acima das abas, sempre visível)
    # ==================================================================
    even_desc = models.CharField(max_length=120, blank=True, null=True)
    even_inativo = models.BooleanField(blank=True, null=True)

    # ==================================================================
    # 📊 ABA 1 — INCIDÊNCIA
    # ==================================================================
    # Classificação / Natureza
    even_classificacao = models.CharField(max_length=30, blank=True, null=True)
    even_natureza_rubrica = models.CharField(
        max_length=6, blank=True, null=True, choices=NATUREZA_RUBRICA_CHOICES
    )

    # Tipos / Referência
    even_tipo_referencia = models.IntegerField(
        blank=True, null=True, choices=TIPO_REFERENCIA_CHOICES
    )
    even_tipo_verba = models.IntegerField(
        blank=True, null=True, choices=TIPO_VERBA_CHOICES
    )

    # Incidências tributárias (flags booleanas como no legado)
    even_incide_inss = models.BooleanField(blank=True, null=True)
    even_incide_fgts = models.BooleanField(blank=True, null=True)
    even_incide_ir = models.BooleanField(blank=True, null=True)
    even_incide_pis_pasep = models.BooleanField(blank=True, null=True)
    even_incide_contribuicoes_sindicais = models.BooleanField(blank=True, null=True)
    even_incide_base_salario_familia = models.BooleanField(blank=True, null=True)

    # Códigos eSocial (4 entradas independentes, como no legado)
    even_esocial_1 = models.CharField(max_length=6, blank=True, null=True)
    even_esocial_2 = models.CharField(max_length=6, blank=True, null=True)
    even_esocial_3 = models.CharField(max_length=6, blank=True, null=True)
    even_esocial_4 = models.CharField(max_length=6, blank=True, null=True)

    # ==================================================================
    # ⚙️ ABA 2 — CARACTERÍSTICAS
    # ==================================================================
    # Horas extras (campo especial: checkbox + % + símbolo %)
    even_flag_horas_extras = models.BooleanField(blank=True, null=True)
    even_percentual_horas_extras = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )

    # Outros flags booleanos (27 flags exatamente como no legado / SQL)
    even_rendimento_variavel = models.BooleanField(blank=True, null=True)
    even_comissao = models.BooleanField(blank=True, null=True)
    even_dsr_salario = models.BooleanField(blank=True, null=True)
    even_dsr_horas_extras = models.BooleanField(blank=True, null=True)
    even_dsr_rendimentos_variaveis = models.BooleanField(blank=True, null=True)
    even_indenizacao_rescisao_contrato = models.BooleanField(blank=True, null=True)
    even_ajuda_custo_diarias = models.BooleanField(blank=True, null=True)
    even_grava_ficha_horas_normais = models.BooleanField(blank=True, null=True)
    even_adicional_dirigente_sindical = models.BooleanField(blank=True, null=True)
    even_media_horas_adicional_noturno = models.BooleanField(blank=True, null=True)
    even_plano_saude_empresarial = models.BooleanField(blank=True, null=True)
    even_reembolso_despesas_medicas = models.BooleanField(blank=True, null=True)
    even_despesas_judiciarias = models.BooleanField(blank=True, null=True)
    even_distribuicao_lucros = models.BooleanField(blank=True, null=True)
    even_previdencia_privada = models.BooleanField(blank=True, null=True)
    even_fapi = models.BooleanField(blank=True, null=True)
    even_pensao_alimenticia = models.BooleanField(blank=True, null=True)
    even_previdencia_oficial = models.BooleanField(blank=True, null=True)
    even_desconto_compulsorio = models.BooleanField(blank=True, null=True)
    even_salario_garantia = models.BooleanField(blank=True, null=True)
    even_taxa_servico = models.BooleanField(blank=True, null=True)
    even_medias_sobre_valores = models.BooleanField(blank=True, null=True)
    even_somente_tomador_principal = models.BooleanField(blank=True, null=True)
    even_rendimento_isento_irrf = models.BooleanField(blank=True, null=True)
    even_nao_considera_para_estouro = models.BooleanField(blank=True, null=True)
    even_descontar_pensao_paga_13 = models.BooleanField(blank=True, null=True)
    even_descontar_pensao_paga_adto13 = models.BooleanField(blank=True, null=True)
    even_imprimir_verba_zerada = models.BooleanField(blank=True, null=True)
    even_ferias_folha_credito_trabalha = models.BooleanField(blank=True, null=True)

    # Órgão público
    even_teto_remuneratorio_cf = models.IntegerField(
        blank=True, null=True, choices=TETO_REMUNERATORIO_CHOICES
    )
    even_incidencia_cprp = models.IntegerField(
        blank=True, null=True, choices=INCIDENCIA_CPRP_CHOICES
    )
    even_funcionarios_afastados = models.IntegerField(
        blank=True, null=True, choices=FUNCIONARIOS_AFASTADOS_CHOICES
    )

    even_verba_negativa_esocial = models.CharField(max_length=6, blank=True, null=True)

    # Observação
    even_observacao = models.TextField(blank=True, null=True)

    # ==================================================================
    # 🧮 ABA 3 — FÓRMULAS
    # ==================================================================
    even_formula_ref1 = models.CharField(max_length=200, blank=True, null=True)
    even_formula_ref2 = models.CharField(max_length=200, blank=True, null=True)
    even_formula_ref3 = models.CharField(max_length=200, blank=True, null=True)
    even_formula_valo1 = models.CharField(max_length=200, blank=True, null=True)
    even_formula_valo2 = models.CharField(max_length=200, blank=True, null=True)
    even_formula_valo3 = models.CharField(max_length=200, blank=True, null=True)

    # ==================================================================
    # 🗂️ Controle de auditoria (legado — colunas físicas)
    # ==================================================================
    even_log_data = models.DateField(db_column="_log_data", blank=True, null=True)
    even_log_hora = models.TimeField(db_column="_log_time", blank=True, null=True)

    # ==================================================================
    objects = BancoConsulta()

    # ------------------------------------------------------------------
    # Controle de chave composta nos métodos save() / delete()
    # (mesmo padrão do modelo Funcionarios)
    # ------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_chave_composta = self._get_chave_composta()

    def _get_chave_composta(self):
        return {
            "registro": self.registro,
            "even_empr": self.even_empr,
            "even_codi": self.even_codi,
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
        updated = (
            self.__class__.objects.using(using)
            .filter(**self._original_chave_composta)
            .update(**valores)
        )
        if not updated:
            raise self.__class__.DoesNotExist(
                "Evento nao encontrado para atualizacao."
            )

        self._original_chave_composta = self._get_chave_composta()

    def delete(self, using=None, keep_parents=False):
        using = using or self._state.db
        deleted_count, _ = (
            self.__class__.objects.using(using)
            .filter(**self._get_chave_composta())
            .delete()
        )
        return deleted_count, {}

    class Meta:
        managed = False
        db_table = "eventos"
        unique_together = (("registro", "even_empr", "even_codi"),)
