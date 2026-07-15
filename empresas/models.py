from django.db import models

from core.consultas import BancoConsulta


class Empresas(models.Model):
    # Django 2.2 nao oferece suporte nativo a chave primaria composta.
    # Mantemos `registro` como chave tecnica do ORM para evitar a criacao de um
    # `id` inexistente na tabela, mas toda operacao de escrita deve respeitar a
    # chave real: (registro, empr_empr, empr_fili).
    registro = models.CharField(primary_key=True, max_length=14)
    empr_empr = models.IntegerField()
    empr_fili = models.IntegerField()

    # Cadastrais
    empr_nome = models.CharField(max_length=200)
    empr_fant = models.CharField(max_length=200, blank=True, null=True)
    empr_data_cada = models.DateField(blank=True, null=True)
    empr_situ = models.IntegerField(blank=True, null=True)
    empr_tipo_estab = models.IntegerField(blank=True, null=True)
    empr_tipo_docu = models.IntegerField(blank=True, null=True)
    empr_tipo_docu_aux = models.IntegerField(blank=True, null=True)
    empr_cnpj = models.CharField(max_length=14, blank=True, null=True)
    empr_cpf = models.CharField(max_length=11, blank=True, null=True)
    empr_tipo_caepf = models.IntegerField(blank=True, null=True)
    empr_caepf = models.CharField(max_length=14, blank=True, null=True)
    empr_escr_muni = models.CharField(max_length=25, blank=True, null=True)
    empr_insc_esta = models.CharField(max_length=25, blank=True, null=True)
    empr_inic_ativ = models.DateField(blank=True, null=True)
    empr_fim_ativ = models.DateField(blank=True, null=True)
    empr_indi_situ = models.IntegerField(blank=True, null=True)
    empr_capi_soci = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    empr_espec_estab = models.CharField(max_length=60, blank=True, null=True)
    empr_soci_oste = models.BooleanField(blank=True, null=True)

    # Endereco
    empr_cep = models.CharField(max_length=8, blank=True, null=True)
    empr_logr = models.IntegerField(blank=True, null=True)
    empr_ende = models.CharField(max_length=120, blank=True, null=True)
    empr_ende_nume = models.CharField(max_length=20, blank=True, null=True)
    empr_ende_comp = models.CharField(max_length=60, blank=True, null=True)
    empr_ende_bair = models.CharField(max_length=60, blank=True, null=True)
    empr_ende_cida = models.CharField(max_length=60, blank=True, null=True)
    empr_ende_uf = models.CharField(max_length=2, blank=True, null=True)
    empr_ende_fone1 = models.CharField(max_length=14, blank=True, null=True)
    empr_ende_fone2 = models.CharField(max_length=14, blank=True, null=True)
    empr_ende_celu = models.CharField(max_length=14, blank=True, null=True)
    empr_ende_emai = models.CharField(max_length=200, blank=True, null=True)

    # GPS / Tributacao
    empr_enqu_fede = models.IntegerField(blank=True, null=True)
    empr_prest_serv_anex_v_iv = models.IntegerField(blank=True, null=True)
    empr_simp_opta = models.IntegerField(blank=True, null=True)
    empr_ativ_simp_naci = models.BooleanField(blank=True, null=True)
    empr_cecu_ativ_simp_naci = models.BooleanField(blank=True, null=True)
    empr_part_pbm = models.BooleanField(blank=True, null=True)
    empr_cecu_part_pbm = models.BooleanField(blank=True, null=True)
    empr_constutora = models.BooleanField(blank=True, null=True)
    empr_codi_paga = models.IntegerField(blank=True, null=True)
    empr_codi_paga_funrural = models.IntegerField(blank=True, null=True)
    empr_codi_paga_transp = models.IntegerField(blank=True, null=True)
    empr_codi_terc = models.IntegerField(blank=True, null=True)
    empr_fpas = models.IntegerField(blank=True, null=True)
    empr_perc_fpas = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    empr_class_trib = models.IntegerField(blank=True, null=True)
    empr_codi_lota_trib = models.IntegerField(blank=True, null=True)
    empr_cnae_prep = models.IntegerField(blank=True, null=True)
    empr_cnae = models.CharField(max_length=10, blank=True, null=True)
    empr_perc_rat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    empr_perc_empregadores = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    empr_perc_fap = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    empr_perc_auto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    empr_rete_nf = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    empr_perc_empregados = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Parametros Gerais 1
    empr_perc_pis_folha = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    empr_fechamento_mes = models.IntegerField(blank=True, null=True)
    empr_fechamento_vale_transporte = models.IntegerField(blank=True, null=True)
    empr_tabela_inss = models.CharField(max_length=6, blank=True, null=True)
    empr_tabela_irrf = models.CharField(max_length=6, blank=True, null=True)
    empr_tabela_irrf_plr = models.CharField(max_length=6, blank=True, null=True)
    empr_estouro = models.BooleanField(blank=True, null=True)
    empr_estouro_rescisao = models.BooleanField(blank=True, null=True)
    empr_etiqueta = models.BooleanField(blank=True, null=True)
    empr_ignora_faltas = models.BooleanField(blank=True, null=True)
    empr_ignora_faltas_decimo_terceiro = models.BooleanField(blank=True, null=True)
    empr_taxa_servico = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    empr_centro_custo_departamento = models.BooleanField(blank=True, null=True)
    empr_mes_competencia_folha = models.IntegerField(blank=True, null=True)
    empr_calcula_ir_adiantamento_salarial = models.BooleanField(blank=True, null=True)
    empr_ir_adiantamento_detalhado = models.BooleanField(blank=True, null=True)
    empr_arredondamento_centavos = models.IntegerField(blank=True, null=True)
    empr_arredondamento_tipo = models.IntegerField(blank=True, null=True)
    empr_grava_arredondamento_proximo_mes = models.BooleanField(blank=True, null=True)
    empr_proporcionalidade_admissao = models.IntegerField(blank=True, null=True)
    empr_proporcionalidade_rescisao = models.IntegerField(blank=True, null=True)
    empr_tipo_calculo_ferias = models.IntegerField(blank=True, null=True)
    empr_ferias_mensal_somente_salario = models.BooleanField(blank=True, null=True)
    empr_ferias_rescisao_mes_nao_integral = models.BooleanField(blank=True, null=True)
    empr_ferias_paga_integral_rescisao = models.BooleanField(blank=True, null=True)
    empr_tipo_calculo_adiantamento_13 = models.IntegerField(blank=True, null=True)
    empr_adiantamento_13_mensal_somente_salario = models.BooleanField(blank=True, null=True)
    empr_adiantamento_13_rescisao_mes_nao_integral = models.BooleanField(blank=True, null=True)
    empr_adiantamento_13_paga_integral_rescisao = models.BooleanField(blank=True, null=True)

    # Parametros Gerais 2
    empr_ferias_coletivas_muda_periodo_aquisitivo_menos_12_meses = models.BooleanField(blank=True, null=True)
    empr_ferias_coletivas_saldo_inferior_dias_gozo = models.IntegerField(blank=True, null=True)
    empr_ferias_coletivas_funcionarios_mais_12_meses = models.IntegerField(blank=True, null=True)
    empr_nao_considera_faltas_horas_ferias = models.BooleanField(blank=True, null=True)
    empr_arredonda_ferias_cima = models.BooleanField(blank=True, null=True)
    empr_calcula_folhas_tomador = models.BooleanField(blank=True, null=True)
    empr_nao_considera_verbas_exclusivas_tomador_principal = models.BooleanField(blank=True, null=True)
    empr_usa_centro_custo_cadastro_funcionario_13_salario = models.BooleanField(blank=True, null=True)
    empr_horas_apura_rateio_quadro_horarios = models.BooleanField(blank=True, null=True)
    empr_agrupar_centros_custo_mesmo_cnpj_cei = models.BooleanField(blank=True, null=True)
    empr_pagar_somente_abono_ferias = models.BooleanField(blank=True, null=True)
    empr_controla_pagamento_salario_familia = models.BooleanField(blank=True, null=True)
    empr_nao_prorroga_periodo_aquisitivo_bem = models.BooleanField(blank=True, null=True)
    empr_converter_referencia_horas = models.BooleanField(blank=True, null=True)
    empr_converter_referencia_horas_noturnas = models.BooleanField(blank=True, null=True)
    empr_converter_referencia_centesimal_planilhas = models.BooleanField(blank=True, null=True)
    empr_sindicalizada = models.BooleanField(blank=True, null=True)
    empr_nao_lanca_compensacao_reembolso = models.BooleanField(blank=True, null=True)
    empr_controla_contas_bancarias_funcionarios = models.BooleanField(blank=True, null=True)
    empr_pagar_decimo_terceiro_complementar_folha_normal = models.BooleanField(blank=True, null=True)
    empr_pagar_decimo_terceiro_integral_bem = models.BooleanField(blank=True, null=True)
    empr_perc_adiantamento_salario = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    empr_primeira_declaracao_caged = models.CharField(max_length=10, blank=True, null=True)
    empr_medias = models.IntegerField(blank=True, null=True)
    empr_mensagem_aniversario = models.IntegerField(blank=True, null=True)
    empr_prazo_experiencia = models.IntegerField(blank=True, null=True)
    empr_contabilizacao = models.IntegerField(blank=True, null=True)
    empr_emissao_guias = models.IntegerField(blank=True, null=True)
    empr_sefip = models.IntegerField(blank=True, null=True)
    empr_proporcionalidade_ferias = models.IntegerField(blank=True, null=True)
    empr_proporcionalidade_situacao = models.IntegerField(blank=True, null=True)
    empr_proporcionalidade_adiantamento = models.IntegerField(blank=True, null=True)
    empr_proporcionalidade_tomador = models.IntegerField(blank=True, null=True)

    # Verbas
    empr_verba_mensalista = models.IntegerField(blank=True, null=True)
    empr_verba_mensalista_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_diarista = models.IntegerField(blank=True, null=True)
    empr_verba_diarista_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_horista = models.IntegerField(blank=True, null=True)
    empr_verba_horista_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_horista_especial = models.IntegerField(blank=True, null=True)
    empr_verba_horista_especial_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_pro_labore = models.IntegerField(blank=True, null=True)
    empr_verba_pro_labore_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_pro_labore_fgts = models.IntegerField(blank=True, null=True)
    empr_verba_pro_labore_fgts_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_estagiario = models.IntegerField(blank=True, null=True)
    empr_verba_estagiario_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_aposentado = models.IntegerField(blank=True, null=True)
    empr_verba_aposentado_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_tarefeiro = models.IntegerField(blank=True, null=True)
    empr_verba_tarefeiro_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_iss = models.IntegerField(blank=True, null=True)
    empr_verba_iss_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_contribuicao_sest = models.IntegerField(blank=True, null=True)
    empr_verba_contribuicao_sest_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_contribuicao_senat = models.IntegerField(blank=True, null=True)
    empr_verba_contribuicao_senat_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_intermitente = models.IntegerField(blank=True, null=True)
    empr_verba_intermitente_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_domestica_fgts = models.IntegerField(blank=True, null=True)
    empr_verba_domestica_fgts_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_domestica_sem_fgts = models.IntegerField(blank=True, null=True)
    empr_verba_domestica_sem_fgts_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_autonomo = models.IntegerField(blank=True, null=True)
    empr_verba_autonomo_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_comissionado = models.IntegerField(blank=True, null=True)
    empr_verba_comissionado_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_pagamento_semanal = models.IntegerField(blank=True, null=True)
    empr_verba_pagamento_semanal_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_pagamento_semanal_pro = models.IntegerField(blank=True, null=True)
    empr_verba_pagamento_semanal_pro_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_pagamento_semanal_aut = models.IntegerField(blank=True, null=True)
    empr_verba_pagamento_semanal_aut_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_plr = models.IntegerField(blank=True, null=True)
    empr_verba_plr_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_pagamento_quinzenal = models.IntegerField(blank=True, null=True)
    empr_verba_pagamento_quinzenal_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_pagamento_quinzenal_pro = models.IntegerField(blank=True, null=True)
    empr_verba_pagamento_quinzenal_pro_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_pagamento_quinzenal_aut = models.IntegerField(blank=True, null=True)
    empr_verba_pagamento_quinzenal_aut_desc = models.CharField(max_length=120, blank=True, null=True)
    empr_verba_multa_verde_amarelo = models.IntegerField(blank=True, null=True)
    empr_verba_multa_verde_amarelo_desc = models.CharField(max_length=120, blank=True, null=True)

    # Observacoes
    empr_obse = models.TextField(blank=True, null=True)

    objects = BancoConsulta()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_chave_composta = self._get_chave_composta()

    def _get_chave_composta(self):
        return {
            "registro": self.registro,
            "empr_empr": self.empr_empr,
            "empr_fili": self.empr_fili,
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
            raise self.__class__.DoesNotExist("Empresa nao encontrada para atualizacao.")

        self._original_chave_composta = self._get_chave_composta()

    def delete(self, using=None, keep_parents=False):
        using = using or self._state.db
        deleted_count, _ = self.__class__.objects.using(using).filter(
            **self._get_chave_composta()
        ).delete()
        return deleted_count, {}

    class Meta:
        managed = False
        db_table = "empresas"
        unique_together = (("registro", "empr_empr", "empr_fili"),)
