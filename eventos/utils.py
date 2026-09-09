ABA_CAMPOS = {
    "incidencia": [
        "even_classificacao",
        "even_natureza_rubrica",
        "even_tipo_referencia",
        "even_tipo_verba",
        "even_incide_inss",
        "even_incide_fgts",
        "even_incide_ir",
        "even_incide_pis_pasep",
        "even_incide_contribuicoes_sindicais",
        "even_incide_base_salario_familia",
        "even_esocial_1",
        "even_esocial_2",
        "even_esocial_3",
        "even_esocial_4",
    ],
    "caracteristicas": [
        "even_flag_horas_extras",
        "even_percentual_horas_extras",
        "even_rendimento_variavel",
        "even_comissao",
        "even_dsr_salario",
        "even_dsr_horas_extras",
        "even_dsr_rendimentos_variaveis",
        "even_indenizacao_rescisao_contrato",
        "even_ajuda_custo_diarias",
        "even_grava_ficha_horas_normais",
        "even_adicional_dirigente_sindical",
        "even_media_horas_adicional_noturno",
        "even_plano_saude_empresarial",
        "even_reembolso_despesas_medicas",
        "even_despesas_judiciarias",
        "even_distribuicao_lucros",
        "even_previdencia_privada",
        "even_fapi",
        "even_pensao_alimenticia",
        "even_previdencia_oficial",
        "even_desconto_compulsorio",
        "even_salario_garantia",
        "even_taxa_servico",
        "even_medias_sobre_valores",
        "even_somente_tomador_principal",
        "even_rendimento_isento_irrf",
        "even_nao_considera_para_estouro",
        "even_descontar_pensao_paga_13",
        "even_descontar_pensao_paga_adto13",
        "even_imprimir_verba_zerada",
        "even_ferias_folha_credito_trabalha",
        "even_teto_remuneratorio_cf",
        "even_incidencia_cprp",
        "even_funcionarios_afastados",
        "even_verba_negativa_esocial",
        "even_observacao",
    ],
    "formulas": [
        "even_formula_ref1",
        "even_formula_ref2",
        "even_formula_ref3",
        "even_formula_valo1",
        "even_formula_valo2",
        "even_formula_valo3",
    ],
}


def _has_errors(form):
    erros = set(form.errors.keys())

    por_aba = {aba: bool(erros & set(campos)) for aba, campos in ABA_CAMPOS.items()}

    campos_de_todas_abas = {c for lista in ABA_CAMPOS.values() for c in lista}
    por_aba["cabecalho"] = bool(erros - campos_de_todas_abas)

    return por_aba
