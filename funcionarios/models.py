from django.db import models

from core.consultas import BancoConsulta


class Funcionarios(models.Model):
    # Django 2.2 nao oferece suporte nativo a chave primaria composta.
    # Mantemos `registro` como chave tecnica do ORM para evitar um `id`
    # inexistente na tabela, mas toda escrita deve respeitar a chave real:
    # (registro, func_empr, func_codi, func_fili).
    registro = models.CharField(primary_key=True, max_length=14)
    func_empr = models.IntegerField()
    func_codi = models.IntegerField()
    func_fili = models.IntegerField()

    # Cadastrais > Pessoais
    func_admissao_preliminar = models.IntegerField(blank=True, null=True)
    func_integracao_esocial = models.BooleanField(blank=True, null=True)
    func_nome = models.CharField(max_length=200)
    func_email = models.CharField(max_length=200, blank=True, null=True)
    func_ddd = models.CharField(max_length=4, blank=True, null=True)
    func_telefone = models.CharField(max_length=20, blank=True, null=True)
    func_ddd_celular = models.CharField(max_length=4, blank=True, null=True)
    func_celular = models.CharField(max_length=20, blank=True, null=True)
    func_nascimento = models.DateField(blank=True, null=True)
    func_pais_nascimento = models.CharField(max_length=7, blank=True, null=True)
    func_cidade_nascimento = models.CharField(max_length=60, blank=True, null=True)
    func_naturalidade = models.CharField(max_length=2, blank=True, null=True)
    func_grau_instrucao = models.CharField(max_length=2, blank=True, null=True)
    func_ficha_registro = models.CharField(max_length=20, blank=True, null=True)
    func_livro = models.CharField(max_length=20, blank=True, null=True)
    func_folha = models.CharField(max_length=20, blank=True, null=True)
    func_cartao_ponto = models.CharField(max_length=20, blank=True, null=True)
    func_matricula_esocial = models.CharField(max_length=30, blank=True, null=True)
    func_foto_3x4 = models.BinaryField(blank=True, null=True)

    # Cadastrais > Endereco
    func_cep = models.CharField(max_length=8, blank=True, null=True)
    func_logr = models.IntegerField(blank=True, null=True)
    func_ende = models.CharField(max_length=120, blank=True, null=True)
    func_ende_nume = models.CharField(max_length=20, blank=True, null=True)
    func_ende_comp = models.CharField(max_length=60, blank=True, null=True)
    func_ende_bair = models.CharField(max_length=60, blank=True, null=True)
    func_ende_cida = models.CharField(max_length=60, blank=True, null=True)
    func_ende_uf = models.CharField(max_length=2, blank=True, null=True)

    # Fisicos
    func_tipo_sanguineo = models.CharField(max_length=5, blank=True, null=True)
    func_etnia_raca = models.IntegerField(blank=True, null=True)
    func_sexo = models.CharField(max_length=1, blank=True, null=True)
    func_pessoa_com_deficiencia = models.BooleanField(blank=True, null=True)
    func_deficiencia_fisica = models.BooleanField(blank=True, null=True)
    func_deficiencia_visual = models.BooleanField(blank=True, null=True)
    func_deficiencia_auditiva = models.BooleanField(blank=True, null=True)
    func_deficiencia_mental = models.BooleanField(blank=True, null=True)
    func_deficiencia_intelectual = models.BooleanField(blank=True, null=True)
    func_reabilitado = models.BooleanField(blank=True, null=True)
    func_cota_deficiencia = models.IntegerField(blank=True, null=True)
    func_observacoes_deficiencias = models.TextField(blank=True, null=True)

    # Historico > Admissionais
    func_admissao = models.DateField(blank=True, null=True)
    func_cadastro = models.DateField(blank=True, null=True)
    func_inicio_adicional_tempo_servico = models.DateField(blank=True, null=True)
    func_alvara_judicial_contratacao_menores = models.BooleanField(blank=True, null=True)
    func_numero_processo = models.CharField(max_length=30, blank=True, null=True)
    func_tipo_admissao = models.IntegerField(blank=True, null=True)
    func_indicativo_admissao = models.IntegerField(blank=True, null=True)
    func_data_aposentadoria = models.DateField(blank=True, null=True)
    func_nova_data_admissao = models.DateField(blank=True, null=True)
    func_numero_processo_rt = models.CharField(max_length=30, blank=True, null=True)
    func_tipo_provimento = models.IntegerField(blank=True, null=True)
    func_natureza_ocupacao = models.IntegerField(blank=True, null=True)
    func_empresa_anterior_cnpj_cpf = models.CharField(max_length=14, blank=True, null=True)
    func_matricula_anterior = models.CharField(max_length=30, blank=True, null=True)
    func_data_transferencia = models.DateField(blank=True, null=True)
    func_transferencia_com_onus = models.BooleanField(blank=True, null=True)
    func_data_saida = models.DateField(blank=True, null=True)
    func_aviso_previo = models.DateField(blank=True, null=True)
    func_motivo_saida = models.TextField(blank=True, null=True)

    # Historico > Contratuais
    func_tipo_contrato_trabalho = models.IntegerField(blank=True, null=True)
    func_indicativo_contratacao = models.TextField(blank=True, null=True)
    func_prazo_experiencia_dias = models.IntegerField(blank=True, null=True)
    func_fim_primeiro_prazo = models.DateField(blank=True, null=True)
    func_termino_ocorrencia_fato = models.DateField(blank=True, null=True)
    func_prorrogacao_dias = models.IntegerField(blank=True, null=True)
    func_fim_prorrogacao = models.DateField(blank=True, null=True)

    # Estrangeiro
    func_pais_nacionalidade = models.CharField(max_length=7, blank=True, null=True)
    func_chegada_brasil = models.DateField(blank=True, null=True)
    func_casado_brasileiro = models.BooleanField(blank=True, null=True)
    func_tem_filhos_brasileiros = models.BooleanField(blank=True, null=True)
    func_rne = models.CharField(max_length=20, blank=True, null=True)
    func_orgao_uf_emissao_rne = models.CharField(max_length=30, blank=True, null=True)
    func_emissao_rne = models.DateField(blank=True, null=True)
    func_tempo_residencia = models.IntegerField(blank=True, null=True)
    func_condicao_ingresso = models.IntegerField(blank=True, null=True)

    # Documentos
    func_cpf = models.CharField(max_length=11, blank=True, null=True)
    func_pis = models.CharField(max_length=14, blank=True, null=True)
    func_emissao_pis = models.DateField(blank=True, null=True)
    func_rg = models.CharField(max_length=20, blank=True, null=True)
    func_orgao_emissor_rg = models.CharField(max_length=20, blank=True, null=True)
    func_uf_rg = models.CharField(max_length=2, blank=True, null=True)
    func_emissao_rg = models.DateField(blank=True, null=True)
    func_carteira_trabalho = models.CharField(max_length=20, blank=True, null=True)
    func_serie_carteira_trabalho = models.CharField(max_length=10, blank=True, null=True)
    func_digito_serie_carteira_trabalho = models.CharField(max_length=2, blank=True, null=True)
    func_uf_carteira_trabalho = models.CharField(max_length=2, blank=True, null=True)
    func_emissao_carteira_trabalho = models.DateField(blank=True, null=True)
    func_cnh = models.CharField(max_length=20, blank=True, null=True)
    func_categoria_cnh = models.CharField(max_length=5, blank=True, null=True)
    func_uf_cnh = models.CharField(max_length=2, blank=True, null=True)
    func_emissao_cnh = models.DateField(blank=True, null=True)
    func_vencimento_cnh = models.DateField(blank=True, null=True)
    func_primeira_habilitacao = models.DateField(blank=True, null=True)
    func_titulo_eleitor = models.CharField(max_length=20, blank=True, null=True)
    func_zona_titulo_eleitor = models.CharField(max_length=5, blank=True, null=True)
    func_secao_titulo_eleitor = models.CharField(max_length=5, blank=True, null=True)
    func_certificado_reservista = models.CharField(max_length=30, blank=True, null=True)
    func_certidao_civil = models.CharField(max_length=30, blank=True, null=True)
    func_tipo_certidao = models.IntegerField(blank=True, null=True)
    func_emissao_certidao = models.DateField(blank=True, null=True)
    func_termo_matricula = models.CharField(max_length=50, blank=True, null=True)
    func_livro_certidao = models.CharField(max_length=20, blank=True, null=True)
    func_folha_certidao = models.CharField(max_length=20, blank=True, null=True)
    func_cartorio = models.CharField(max_length=120, blank=True, null=True)
    func_cidade_cartorio = models.CharField(max_length=7, blank=True, null=True)
    func_uf_cartorio = models.CharField(max_length=2, blank=True, null=True)

    # Parentes
    func_nome_pai = models.CharField(max_length=200, blank=True, null=True)
    func_nome_mae = models.CharField(max_length=200, blank=True, null=True)
    func_estado_civil = models.IntegerField(blank=True, null=True)
    func_nome_conjuge = models.CharField(max_length=200, blank=True, null=True)
    func_dependentes = models.BooleanField(blank=True, null=True)

    # FGTS / GPS
    func_data_opcao = models.DateField(blank=True, null=True)
    func_categoria_sefip = models.IntegerField(blank=True, null=True)
    func_categoria_esocial = models.IntegerField(blank=True, null=True)
    func_grau_risco = models.IntegerField(blank=True, null=True)
    func_percentual_fgts = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    func_rat_aposentadoria = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    func_regime_previdenciario = models.IntegerField(blank=True, null=True)
    func_regime_trabalhista = models.IntegerField(blank=True, null=True)
    func_categoria_origem = models.IntegerField(blank=True, null=True)
    func_tipo_origem_inscricao = models.IntegerField(blank=True, null=True)
    func_cnpj_origem = models.CharField(max_length=14, blank=True, null=True)
    func_admissao_origem = models.DateField(blank=True, null=True)
    func_matricula_origem = models.CharField(max_length=30, blank=True, null=True)
    func_remuneracao_cargo_eletivo = models.IntegerField(blank=True, null=True)
    func_regime_trabalhista_origem = models.IntegerField(blank=True, null=True)
    func_regime_previdenciario_origem = models.IntegerField(blank=True, null=True)
    func_plano_segregacao = models.IntegerField(blank=True, null=True)
    func_teto_rgps = models.IntegerField(blank=True, null=True)
    func_abono_permanencia = models.IntegerField(blank=True, null=True)
    func_inicio_abono = models.DateField(blank=True, null=True)

    # Vinculos
    func_classe = models.IntegerField(blank=True, null=True)
    func_sindicato = models.IntegerField(blank=True, null=True)
    func_vinculo_empregaticio = models.IntegerField(blank=True, null=True)
    func_departamento = models.IntegerField(blank=True, null=True)
    func_centro_custo = models.IntegerField(blank=True, null=True)
    func_cargo = models.IntegerField(blank=True, null=True)
    func_nivel = models.IntegerField(blank=True, null=True)
    func_cbo_cargo = models.CharField(max_length=10, blank=True, null=True)
    func_funcao = models.IntegerField(blank=True, null=True)
    func_cbo_funcao = models.CharField(max_length=10, blank=True, null=True)
    func_acumulacao_cargo = models.IntegerField(blank=True, null=True)
    func_orgao_classe = models.BooleanField(blank=True, null=True)
    func_inscricao_orgao_classe = models.CharField(max_length=30, blank=True, null=True)
    func_orgao_uf_emissao_orgao_classe = models.CharField(max_length=30, blank=True, null=True)
    func_emissao_orgao_classe = models.DateField(blank=True, null=True)
    func_validade_orgao_classe = models.DateField(blank=True, null=True)

    # Calculo
    func_horas_mes = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    func_horas_semana = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    func_horas_dia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    func_forma_pagamento = models.IntegerField(blank=True, null=True)
    func_tipo_funcionario = models.IntegerField(blank=True, null=True)
    func_salario_base = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_comissao = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    func_adic_insalubridade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    func_incidencia_insalubridade = models.IntegerField(blank=True, null=True)
    func_adic_periculosidade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    func_incidencia_periculosidade = models.IntegerField(blank=True, null=True)
    func_adicional_noturno = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    func_incidencia_adicional_noturno = models.IntegerField(blank=True, null=True)
    func_vale_alimentacao_compra = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_recebe_dsr_horas_extras = models.BooleanField(blank=True, null=True)
    func_dsr_horas_extras = models.IntegerField(blank=True, null=True)
    func_recebe_dsr_rendimentos_variaveis = models.BooleanField(blank=True, null=True)
    func_dsr_rendimentos_variaveis = models.IntegerField(blank=True, null=True)
    func_recebe_dsr_salarios = models.BooleanField(blank=True, null=True)
    func_dsr_salarios = models.IntegerField(blank=True, null=True)
    func_ignora_faltas_ferias = models.BooleanField(blank=True, null=True)
    func_imprimir_etiqueta = models.BooleanField(blank=True, null=True)
    func_regime_tempo_parcial = models.BooleanField(blank=True, null=True)
    func_nao_arredondar = models.BooleanField(blank=True, null=True)
    func_salario_contratual_comissionado = models.BooleanField(blank=True, null=True)
    func_adiantamento = models.BooleanField(blank=True, null=True)
    func_valor_fixo_adiantamento = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_aplica_deducao_mais_benefica_irrf = models.BooleanField(blank=True, null=True)
    func_recebe_vale_refeicao = models.BooleanField(blank=True, null=True)
    func_vale_refeicao = models.IntegerField(blank=True, null=True)
    func_cartao_vale_refeicao = models.CharField(max_length=30, blank=True, null=True)
    func_recebe_vale_alimentacao = models.BooleanField(blank=True, null=True)
    func_vale_alimentacao = models.IntegerField(blank=True, null=True)
    func_cartao_vale_alimentacao = models.CharField(max_length=30, blank=True, null=True)

    # Banco
    func_banco = models.CharField(max_length=6, blank=True, null=True)
    func_agencia_pagamento = models.CharField(max_length=20, blank=True, null=True)
    func_conta_pagamento = models.CharField(max_length=30, blank=True, null=True)
    func_digito_conta_pagamento = models.CharField(max_length=5, blank=True, null=True)
    func_tipo_conta = models.IntegerField(blank=True, null=True)
    func_cartao_salario = models.CharField(max_length=30, blank=True, null=True)
    func_modo_pagamento = models.IntegerField(blank=True, null=True)

    # Dados de partida
    func_aquisicao_ferias = models.DateField(blank=True, null=True)
    func_salario_inicial = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_descontar_contribuicao_sindical = models.BooleanField(blank=True, null=True)
    func_sindicalizado = models.BooleanField(blank=True, null=True)
    func_valor_previdencia_privada = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_valor_previdencia_privada_13 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_base_ir = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_valor_ir = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_base_inss_multiplos_vinculos = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_valor_inss_multiplos_vinculos = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_base_inss_multiplos_vinculos_13 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_valor_inss_multiplos_vinculos_13 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_base_ir_multiplos_vinculos = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_valor_ir_multiplos_vinculos = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_base_ir_multiplos_vinculos_13 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    func_valor_ir_multiplos_vinculos_13 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    # Quadro de horarios
    func_vigencia_quadro_horario = models.DateField(blank=True, null=True)
    func_regime_jornada_trabalho = models.IntegerField(blank=True, null=True)
    func_tipo_escala = models.IntegerField(blank=True, null=True)
    func_pre_assinalar_horarios_intervalo = models.BooleanField(blank=True, null=True)
    func_escala = models.CharField(max_length=80, blank=True, null=True)
    func_descanso_semanal = models.IntegerField(blank=True, null=True)
    func_data_inicio_escala = models.DateField(blank=True, null=True)
    func_tipo_revezamento = models.IntegerField(blank=True, null=True)
    func_tipo_jornada_esocial = models.IntegerField(blank=True, null=True)
    func_horario_noturno = models.BooleanField(blank=True, null=True)
    func_folga_inicial = models.IntegerField(blank=True, null=True)

    # eSocial
    func_nit = models.CharField(max_length=11, blank=True, null=True)
    func_qualificacao_cadastral_status = models.TextField(blank=True, null=True)
    func_esocial_integrado = models.BooleanField(blank=True, null=True)
    func_esocial_data_integracao = models.DateTimeField(blank=True, null=True)
    func_esocial_numero_recibo = models.CharField(max_length=40, blank=True, null=True)

    # Outros
    func_ultimo_exame_medico = models.DateField(blank=True, null=True)
    func_proximo_exame_medico_meses = models.IntegerField(blank=True, null=True)
    func_proximo_exame_medico = models.DateField(blank=True, null=True)
    func_ultimo_exame_audiometrico = models.DateField(blank=True, null=True)
    func_proximo_exame_audiometrico_meses = models.IntegerField(blank=True, null=True)
    func_proximo_exame_audiometrico = models.DateField(blank=True, null=True)
    func_aprendiz_gravida = models.BooleanField(blank=True, null=True)
    func_observacoes = models.TextField(blank=True, null=True)

    objects = BancoConsulta()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_chave_composta = self._get_chave_composta()

    def _get_chave_composta(self):
        return {
            "registro": self.registro,
            "func_empr": self.func_empr,
            "func_codi": self.func_codi,
            "func_fili": self.func_fili,
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
            raise self.__class__.DoesNotExist("Funcionario nao encontrado para atualizacao.")

        self._original_chave_composta = self._get_chave_composta()

    def delete(self, using=None, keep_parents=False):
        using = using or self._state.db
        try:
            from dependentesrh.models import Dependentesrh
            registro = getattr(self, 'registro', None)
            empr = getattr(self, 'func_empr', None)
            fili = getattr(self, 'func_fili', None)
            func = getattr(self, 'func_codi', None)
            if registro and empr is not None and fili is not None and func is not None:
                try:
                    qs_dep = Dependentesrh.objects
                    if using:
                        qs_dep = qs_dep.using(using)
                    qs_dep.filter(
                        registro=registro,
                        depe_empr=int(empr),
                        depe_fili=int(fili),
                        depe_func=int(func),
                    ).delete()
                except Exception:
                    pass
        except Exception:
            pass
        deleted_count, _ = self.__class__.objects.using(using).filter(
            **self._get_chave_composta()
        ).delete()
        return deleted_count, {}

    class Meta:
        managed = False
        db_table = "funcionarios"
        unique_together = (("registro", "func_empr", "func_codi", "func_fili"),)


class ClassesFuncionario(models.Model):
    clas_codi = models.IntegerField(primary_key=True)
    clas_desc = models.CharField(max_length=60)
    clas_grupo = models.CharField(max_length=30, blank=True, null=True)
    clas_reducao_base_ir = models.BooleanField(blank=True, null=True)
    field_log_data = models.DateField(db_column="_log_data", blank=True, null=True)
    field_log_time = models.TimeField(db_column="_log_time", blank=True, null=True)

    objects = BancoConsulta()

    class Meta:
        managed = False
        db_table = "classes_funcionario"
