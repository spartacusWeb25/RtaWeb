ABA_CAMPOS = {
    "cadastrais": [
        "contr_empr",
        "contr_fili",
        "contr_codi",
        "contr_nome",
        "contr_email",
        "contr_ddd",
        "contr_telefone",
        "contr_ddd_celular",
        "contr_celular",
        "contr_matricula_esocial",
        "contr_admissao_preliminar",
        # Endereco Brasil
        "contr_cep", "contr_logr", "contr_ende", "contr_ende_nume",
        "contr_ende_comp", "contr_ende_bair", "contr_ende_cida_codi",
        "contr_ende_cida_desc", "contr_ende_uf",
        # Residencia exterior (ABA 1 / aba 4)
        "contr_residencia_exterior",
        "contr_pais_residencia_codi", "contr_pais_residencia_desc",
        "contr_ende_exterior", "contr_ende_exterior_nume",
        "contr_ende_exterior_comp", "contr_ende_exterior_bair",
        "contr_ende_exterior_cidade", "contr_ende_exterior_codigo_postal",
    ],
    "fisico": [
        "contr_tipo_sanguineo",
        "contr_etnia_raca",
        "contr_sexo",
        "contr_pessoa_com_deficiencia",
        "contr_deficiencia_fisica", "contr_deficiencia_visual",
        "contr_deficiencia_auditiva", "contr_deficiencia_mental",
        "contr_deficiencia_intelectual", "contr_reabilitado",
        "contr_foto_3x4",
        "contr_observacoes_deficiencias",
    ],
    "historico": [
        "contr_nascimento",
        "contr_pais_nascimento_codi", "contr_pais_nascimento_desc",
        "contr_cidade_nascimento_codi", "contr_cidade_nascimento_desc",
        "contr_naturalidade",
        "contr_estado_civil",
        "contr_grau_instrucao",
        "contr_nome_pai", "contr_nome_mae",
        # Datas historico legado
        "contr_admissao",             # db_column: contr_data_entrada
        "contr_cadastro",             # db_column: contr_data_cadastro
        "contr_inicio_adicional_tempo_servico",
        "contr_data_saida",           # db_column: contr_data_baixa
        "contr_data_pagamento_baixa",
        "contr_motivo_desligamento",
        "contr_esocial_indicativo_pensao_alimenticia_fgts",
        "contr_pensao_fgts_valor",
        "contr_pensao_fgts_percentual",
        # Inativo / Observacoes gerais
        "contr_inativo",
        "contr_observacoes",
    ],
    "estrangeiro": [
        "contr_tempo_residencia",
        "contr_condicao_ingresso",
        "contr_pais_nacionalidade_codi", "contr_pais_nacionalidade_desc",
        "contr_chegada_brasil",
        "contr_casado_brasileiro",
        "contr_tem_filhos_brasileiros",
        "contr_rne",
        "contr_orgao_uf_emissao_rne",
        "contr_emissao_rne",
    ],
    "documentos": [
        "contr_cpf",
        "contr_nis",
        "contr_emissao_nis",
        "contr_rg",
        "contr_orgao_emissor_rg",
        "contr_uf_rg",
        "contr_emissao_rg",
        "contr_carteira_trabalho",
        "contr_serie_carteira_trabalho",
        "contr_digito_serie_carteira_trabalho",
        "contr_uf_carteira_trabalho",
        "contr_emissao_carteira_trabalho",
        "contr_cnh",
        "contr_categoria_cnh",
        "contr_uf_cnh",
        "contr_emissao_cnh",
        "contr_vencimento_cnh",
        "contr_primeira_habilitacao",
        "contr_titulo_eleitor",
        "contr_zona_titulo",           # db_column: contr_zona_titulo_eleitor
        "contr_secao_titulo",          # db_column: contr_secao_titulo_eleitor
        "contr_certificado_reservista",
        "contr_carteira_identidade_arquivo",
        "contr_aviso_carteira_trabalho_digital",
    ],
    "dependentes": (
        "contr_nome_pai", "contr_nome_mae", "contr_tem_dependentes",
    ),
    "fgts_gps": (
        "contr_categoria_sefip","contr_categoria_esocial","contr_categoria_esocial_desc",
        "contr_transp_autonomo_contribuicao_inss",
        "contr_percentual_contr_ir","contr_data_opcao","contr_percentual_fgts","contr_grau_risco",
        "contr_rat_aposentadoria","contr_descontar_iss","contr_percentual_iss","contr_regime_previdenciario",
        "contr_categoria_origem","contr_tipo_cnpj_cpf_origem","contr_cnpj_cpf_origem",
        "contr_admissao_origem","contr_matricula_origem","contr_regime_previdenciario_origem"
    ),
    "vinculos": (
        "contr_classe","contr_vinculo_empregaticio","contr_vinculo_empregaticio_desc",
        "contr_depto","contr_depto_desc",
        "contr_ccusto","contr_ccusto_desc",
        "contr_cargo","contr_cargo_desc",
        "contr_cbo","contr_cbo_desc",
        "contr_natureza_ocupacao",
        "contr_orgao_classe","contr_inscricao_orgao_classe","contr_orgao_uf_emissao_orgao_classe",
        "contr_emissao_orgao_classe","contr_validade_orgao_classe"
    ),
    "calculo": (
        "contr_forma_pagamento","contr_remuneracao","contr_nao_arredondar","contr_descontar_inss_do_ir",
        "contr_adiantamento","contr_valor_previdencia_privada","contr_valor_previdencia_privada_13",
        "contr_aplica_deducao_mais_benefica_irrf",
        "contr_base_inss_multiplos_vinculos","contr_valor_inss_multiplos_vinculos",
        "contr_base_ir_multiplos_vinculos","contr_valor_ir_multiplos_vinculos",
        "contr_base_inss_multiplos_vinculos_13","contr_valor_inss_multiplos_vinculos_13",
        "contr_base_ir_multiplos_vinculos_13","contr_valor_ir_multiplos_vinculos_13"
    ),
    "banco": (
        "contr_banco","contr_banco_desc",
        "contr_conta_corrente","contr_digito_conta_corrente",
        "contr_tipo_conta","contr_modo_pagamento"
    ),
    "esocial": (
        "contr_esocial_qualif_status",
        "contr_esocial_qualif_mensagem",
        "contr_esocial_qualif_data_hora",
        "contr_esocial_integrado",
        "contr_esocial_integra_data_hora",
        "contr_esocial_integra_numero_recibo",
    ),
    "observacoes": ("contr_observacoes",),
}


def _has_errors(form) -> dict:
    campos_com_erro = set(form.errors.keys())
    return {
        aba: bool(campos_com_erro & set(campos))
        for aba, campos in ABA_CAMPOS.items()
    }
