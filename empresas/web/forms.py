import json
from urllib import error as urllib_error
from urllib import request as urllib_request

from django import forms
from django.core.validators import MaxLengthValidator

from core.utils import format_month_reference, get_db_from_slug, normalize_month_reference
from empresas.models import Empresas
from empresas.services.chave import EmpresasChaveService
from tabelainss.models import Tabelainss
from tabelairrf.models import Tabelairrf


CNAE_SUBCLASSES_API_URL = "https://servicodados.ibge.gov.br/api/v2/cnae/subclasses"
CNAE_SUBCLASSE_DETALHE_API_URL = "https://servicodados.ibge.gov.br/api/v2/cnae/subclasses/{codigo}"


def _normalize_cnae_digits(value, pad_left=False):
    digits = "".join(ch for ch in str(value or "") if ch.isdigit())
    if not digits:
        return ""
    if len(digits) > 7:
        return digits[:7]
    if pad_left and len(digits) < 7:
        return digits.zfill(7)
    return digits


def _format_cnae_code(value):
    digits = _normalize_cnae_digits(value, pad_left=True)
    if len(digits) != 7:
        return str(value or "")
    return "{}-{}/{}".format(digits[:4], digits[4], digits[5:])


def _format_cnae_display(value, description=None):
    code = _format_cnae_code(value)
    if not code:
        return ""
    if description:
        return "{} - {}".format(code, description)
    return code


def _format_company_table_reference_display(value):
    raw = str(value or "").strip()
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) == 4:
        month = digits[:2]
        year_suffix = digits[2:]
        if "01" <= month <= "12":
            return "{}/20{}".format(month, year_suffix)
    normalized = normalize_month_reference(raw)
    if normalized:
        return format_month_reference(normalized)
    return raw


def _normalize_company_table_reference_storage(value):
    raw = str(value or "").strip()
    if not raw:
        return ""

    normalized = normalize_month_reference(raw, strict=True)
    return normalized


TAB_FIELD_GROUPS = {
    "cadastrais": (
        "registro",
        "empr_empr",
        "empr_fili",
        "empr_nome",
        "empr_fant",
        "empr_data_cada",
        "empr_situ",
        "empr_tipo_estab",
        "empr_indi_situ",
        "empr_tipo_docu",
        "empr_cnpj",
        "empr_cpf",
        "empr_tipo_docu_aux",
        "empr_tipo_caepf",
        "empr_caepf",
        "empr_escr_muni",
        "empr_insc_esta",
        "empr_capi_soci",
        "empr_inic_ativ",
        "empr_fim_ativ",
        "empr_espec_estab",
        "empr_soci_oste",
    ),
    "endereco": (
        "empr_cep",
        "empr_ende",
        "empr_ende_nume",
        "empr_ende_comp",
        "empr_ende_bair",
        "empr_ende_cida",
        "empr_ende_uf",
        "empr_ende_emai",
        "empr_ende_fone1",
        "empr_ende_fone2",
        "empr_ende_celu",
    ),
    "gps_tributacao": (
        "empr_enqu_fede",
        "empr_prest_serv_anex_v_iv",
        "empr_simp_opta",
        "empr_ativ_simp_naci",
        "empr_cecu_ativ_simp_naci",
        "empr_part_pbm",
        "empr_cecu_part_pbm",
        "empr_constutora",
        "empr_codi_paga",
        "empr_codi_paga_funrural",
        "empr_codi_paga_transp",
        "empr_codi_terc",
        "empr_fpas",
        "empr_perc_fpas",
        "empr_class_trib",
        "empr_codi_lota_trib",
        "empr_cnae_prep",
        "empr_cnae",
        "empr_perc_rat",
        "empr_perc_empregadores",
        "empr_perc_fap",
        "empr_perc_auto",
        "empr_perc_empregados",
        "empr_rete_nf",
    ),
    "parametros1": (
        "empr_perc_pis_folha",
        "empr_fechamento_mes",
        "empr_fechamento_vale_transporte",
        "empr_tabela_inss",
        "empr_tabela_irrf",
        "empr_tabela_irrf_plr",
        "empr_estouro",
        "empr_estouro_rescisao",
        "empr_etiqueta",
        "empr_ignora_faltas",
        "empr_ignora_faltas_decimo_terceiro",
        "empr_taxa_servico",
        "empr_centro_custo_departamento",
        "empr_mes_competencia_folha",
        "empr_calcula_ir_adiantamento_salarial",
        "empr_ir_adiantamento_detalhado",
        "empr_arredondamento_centavos",
        "empr_arredondamento_tipo",
        "empr_grava_arredondamento_proximo_mes",
        "empr_proporcionalidade_admissao",
        "empr_proporcionalidade_rescisao",
        "empr_tipo_calculo_ferias",
        "empr_ferias_mensal_somente_salario",
        "empr_ferias_rescisao_mes_nao_integral",
        "empr_ferias_paga_integral_rescisao",
        "empr_tipo_calculo_adiantamento_13",
        "empr_adiantamento_13_mensal_somente_salario",
        "empr_adiantamento_13_rescisao_mes_nao_integral",
        "empr_adiantamento_13_paga_integral_rescisao",
    ),
    "parametros2": (
        "empr_ferias_coletivas_muda_periodo_aquisitivo_menos_12_meses",
        "empr_ferias_coletivas_saldo_inferior_dias_gozo",
        "empr_ferias_coletivas_funcionarios_mais_12_meses",
        "empr_nao_considera_faltas_horas_ferias",
        "empr_arredonda_ferias_cima",
        "empr_calcula_folhas_tomador",
        "empr_nao_considera_verbas_exclusivas_tomador_principal",
        "empr_usa_centro_custo_cadastro_funcionario_13_salario",
        "empr_horas_apura_rateio_quadro_horarios",
        "empr_agrupar_centros_custo_mesmo_cnpj_cei",
        "empr_pagar_somente_abono_ferias",
        "empr_controla_pagamento_salario_familia",
        "empr_nao_prorroga_periodo_aquisitivo_bem",
        "empr_converter_referencia_horas",
        "empr_converter_referencia_horas_noturnas",
        "empr_converter_referencia_centesimal_planilhas",
        "empr_sindicalizada",
        "empr_nao_lanca_compensacao_reembolso",
        "empr_controla_contas_bancarias_funcionarios",
        "empr_pagar_decimo_terceiro_complementar_folha_normal",
        "empr_pagar_decimo_terceiro_integral_bem",
        "empr_perc_adiantamento_salario",
        "empr_primeira_declaracao_caged",
        "empr_medias",
        "empr_mensagem_aniversario",
        "empr_prazo_experiencia",
        "empr_contabilizacao",
        "empr_emissao_guias",
        "empr_sefip",
        "empr_proporcionalidade_ferias",
        "empr_proporcionalidade_situacao",
        "empr_proporcionalidade_adiantamento",
        "empr_proporcionalidade_tomador",
    ),
    "verbas": (
        "empr_verba_mensalista",
        "empr_verba_mensalista_desc",
        "empr_verba_diarista",
        "empr_verba_diarista_desc",
        "empr_verba_horista",
        "empr_verba_horista_desc",
        "empr_verba_horista_especial",
        "empr_verba_horista_especial_desc",
        "empr_verba_pro_labore",
        "empr_verba_pro_labore_desc",
        "empr_verba_pro_labore_fgts",
        "empr_verba_pro_labore_fgts_desc",
        "empr_verba_estagiario",
        "empr_verba_estagiario_desc",
        "empr_verba_aposentado",
        "empr_verba_aposentado_desc",
        "empr_verba_tarefeiro",
        "empr_verba_tarefeiro_desc",
        "empr_verba_iss",
        "empr_verba_iss_desc",
        "empr_verba_contribuicao_sest",
        "empr_verba_contribuicao_sest_desc",
        "empr_verba_contribuicao_senat",
        "empr_verba_contribuicao_senat_desc",
        "empr_verba_intermitente",
        "empr_verba_intermitente_desc",
        "empr_verba_domestica_fgts",
        "empr_verba_domestica_fgts_desc",
        "empr_verba_domestica_sem_fgts",
        "empr_verba_domestica_sem_fgts_desc",
        "empr_verba_autonomo",
        "empr_verba_autonomo_desc",
        "empr_verba_comissionado",
        "empr_verba_comissionado_desc",
        "empr_verba_pagamento_semanal",
        "empr_verba_pagamento_semanal_desc",
        "empr_verba_pagamento_semanal_pro",
        "empr_verba_pagamento_semanal_pro_desc",
        "empr_verba_pagamento_semanal_aut",
        "empr_verba_pagamento_semanal_aut_desc",
        "empr_verba_plr",
        "empr_verba_plr_desc",
        "empr_verba_pagamento_quinzenal",
        "empr_verba_pagamento_quinzenal_desc",
        "empr_verba_pagamento_quinzenal_pro",
        "empr_verba_pagamento_quinzenal_pro_desc",
        "empr_verba_pagamento_quinzenal_aut",
        "empr_verba_pagamento_quinzenal_aut_desc",
        "empr_verba_multa_verde_amarelo",
        "empr_verba_multa_verde_amarelo_desc",
    ),
    "observacoes": ("empr_obse",),
}

ALL_FIELDS = tuple(field_name for group in TAB_FIELD_GROUPS.values() for field_name in group)
TEXTAREA_FIELDS = {"empr_obse"}
DATE_FIELDS = {"empr_data_cada", "empr_inic_ativ", "empr_fim_ativ"}
DECIMAL_FIELDS = {
    "empr_capi_soci",
    "empr_perc_fpas",
    "empr_perc_rat",
    "empr_perc_empregadores",
    "empr_perc_fap",
    "empr_perc_auto",
    "empr_rete_nf",
    "empr_perc_empregados",
    "empr_perc_pis_folha",
    "empr_taxa_servico",
    "empr_perc_adiantamento_salario",
}
DIGIT_ONLY_FIELDS = {
    "registro",
    "empr_cnpj",
    "empr_cpf",
    "empr_caepf",
    "empr_cep",
    "empr_escr_muni",
    "empr_insc_esta",
    "empr_ende_fone1",
    "empr_ende_fone2",
    "empr_ende_celu",
    "empr_tabela_inss",
    "empr_tabela_irrf",
    "empr_tabela_irrf_plr",
}
EMAIL_FIELDS = {"empr_ende_emai"}
RADIO_CHOICES = {
    "empr_tipo_estab": (
        (1, "Matriz"),
        (2, "Filial"),
        (3, "Outros"),
    ),
    "empr_tipo_docu": (
        (1, "CNPJ"),
        (2, "CEI"),
        (3, "CPF"),
    ),
    "empr_tipo_docu_aux": (
        (1, "CNPJ"),
        (2, "CEI"),
        (3, "CPF"),
    ),
    "empr_tipo_calculo_ferias": (
        (1, "Convencional (anual)"),
        (2, "1/12 (mensal)"),
        (3, "1/30 (diario)"),
    ),
    "empr_tipo_calculo_adiantamento_13": (
        (1, "Convencional (anual)"),
        (2, "1/12 (mensal)"),
        (3, "1/30 (diario)"),
    ),
}
SELECT_CHOICES = {
    "empr_enqu_fede": (
        ("", "Selecione"),
        (1, "Microempresa (ME)"),
        (2, "Empresa de Pequeno Porte (EPP)"),
    ),
    "empr_prest_serv_anex_v_iv": (
        ("", "Selecione"),
        (1, "Sim"),
        (2, "Não"),
    ),
    "empr_mes_competencia_folha": (
        ("", "Selecione"),
        (1, "Mês da competência da folha"),
    ),
    "empr_arredondamento_centavos": (
        ("", "Selecione"),
        (1, "Centavos"),
    ),
    "empr_arredondamento_tipo": (
        ("", "Selecione"),
        (1, "Para cima"),
    ),
    "empr_proporcionalidade_admissao": (
        ("", "Selecione"),
        (1, "Divide por 30 considerando ate o ultimo dia do mes"),
    ),
    "empr_proporcionalidade_rescisao": (
        ("", "Selecione"),
        (1, "Divide por 30 dias"),
    ),
    "empr_ferias_coletivas_saldo_inferior_dias_gozo": (
        ("", "Selecione"),
        (1, "Apenas com saldo inferior aos dias de gozo"),
    ),
    "empr_ferias_coletivas_funcionarios_mais_12_meses": (
        ("", "Selecione"),
        (1, "Calcula conforme periodo de gozo"),
    ),
    "empr_medias": (
        ("", "Selecione"),
        (1, "Divide pela quantidade de meses que o funcionário trabalhou pelo menos 15 dias"),
    ),
    "empr_prazo_experiencia": (
        ("", "Selecione"),
        (1, "Dias"),
    ),
    "empr_contabilizacao": (
        ("", "Selecione"),
        (1, "Departamento"),
    ),
    "empr_emissao_guias": (
        ("", "Selecione"),
        (1, "Departamento"),
    ),
    "empr_sefip": (
        ("", "Selecione"),
        (1, "Centro de custo"),
    ),
    "empr_proporcionalidade_ferias": (
        ("", "Selecione"),
        (1, "Divisão por dias do mês"),
    ),
    "empr_proporcionalidade_situacao": (
        ("", "Selecione"),
        (1, "Divisão por dias do mês"),
    ),
    "empr_proporcionalidade_adiantamento": (
        ("", "Selecione"),
        (1, "Divisão por dias do mês"),
    ),
    "empr_proporcionalidade_tomador": (
        ("", "Selecione"),
        (1, "Divisao por 30"),
    ),
    "empr_codi_paga": (
        ("", "Selecione"),
        (2003, "2003 - Simples - CNPJ"),
        (2100, "2100 - Empresas em Geral - CNPJ"),
        (2119, "2119 - Empresas em Geral - CNPJ - Outras Entidades"),
        (2127, "2127 - Cooperativa de trabalho - CNPJ"),
        (2143, "2143 - Empresas em Geral - CNPJ - FNDE ate 12/2006"),
        (2208, "2208 - Empresas em Geral - CEI"),
        (2216, "2216 - Empresas em Geral - CEI - Outras Entidades"),
        (2240, "2240 - Empresas em Geral - CEI - FNDE ate 12/2006"),
        (2305, "2305 - Filantropicas com Isencao - CNPJ"),
        (2321, "2321 - Filantropicas com Isencao - CEI"),
    ),
    "empr_codi_paga_funrural": (
        ("", "Selecione"),
        (2011, "2011 - Simples - aquisicao de produto rural de produtor rural PF"),
        (2437, "2437 - Orgao do Poder Publico - aquisicao de produto rural de produtor rural PF"),
        (2607, "2607 - Comercializacao da producao rural - CNPJ"),
        (2615, "2615 - Comercializacao da producao rural - CNPJ - SENAR"),
        (2704, "2704 - Comercializacao da producao rural - CEI"),
        (2712, "2712 - Comercializacao da producao rural - CEI - SENAR"),
    ),
    "empr_codi_paga_transp": (
        ("", "Selecione"),
        (2020, "2020 - Simples - contratacao de transportador rodoviario autonomo"),
        (2445, "2445 - Orgao do Poder Publico - contratacao de transportador rodoviario autonomo"),
    ),
    "empr_codi_terc": (
        ("", "Selecione"),
        (79, "79 - sem convenio"),
    ),
    "empr_fpas": (
        ("", "Selecione"),
        (507, "507 - Industria em geral"),
        (515, "515 - Empresas de transporte"),
        (523, "523 - Construcao civil"),
        (531, "531 - Comercio em geral"),
        (540, "540 - Cooperativas"),
        (558, "558 - Prestacao de servicos em geral"),
        (566, "566 - Instituicoes financeiras"),
        (574, "574 - Empresas de comunicacao"),
        (582, "582 - Hospitais e servicos de saude"),
        (590, "590 - Estabelecimentos de ensino"),
        (604, "604 - Agroindustria"),
        (612, "612 - Produtor rural pessoa juridica"),
        (639, "639 - Entidades beneficentes/isentas (situacoes especificas)"),
        (647, "647 - Orgaos publicos e autarquias (situacoes especificas)"),
        (655, "655 - Missoes diplomaticas e organismos internacionais"),
    ),
    "empr_class_trib": (
        ("", "Selecione"),
        (1, "01 - Empresa enquadrada no regime de tributacao Simples Nacional com tributacao previdenciaria substituida"),
        (2, "02 - Empresa enquadrada no regime de tributacao Simples Nacional com tributacao previdenciaria nao substituida"),
        (3, "03 - Empresa enquadrada no regime de tributacao Simples Nacional com tributacao previdenciaria substituida e nao substituida"),
        (4, "04 - Microempreendedor Individual (MEI)"),
        (6, "06 - Agroindustria"),
        (7, "07 - Produtor Rural Pessoa Juridica"),
        (9, "09 - Orgao Gestor de Mao de Obra (OGMO)"),
        (10, "10 - Entidade sindical a que se refere a Lei n 12.023/2009"),
        (11, "11 - Associacao desportiva que mantem clube de futebol profissional"),
        (13, "13 - Banco, caixa economica, sociedade de credito, financiamento e investimento e demais empresas relacionadas no paragrafo 1 do art. 22 da Lei n 8.212/1991"),
        (14, "14 - Sindicatos em geral, exceto os classificados no codigo 10"),
        (21, "21 - Pessoa Fisica, exceto segurado especial"),
        (22, "22 - Segurado especial, inclusive quando for empregador domestico"),
        (60, "60 - Missao diplomatica ou reparticao consular de carreira estrangeira"),
        (70, "70 - Empresa de que trata o Decreto n 5.436/2005"),
        (80, "80 - Entidade beneficente de assistencia social isenta de contribuicoes sociais"),
        (85, "85 - Administracao direta da Uniao, Estados, Distrito Federal e Municipios; autarquias e fundacoes publicas"),
        (99, "99 - Pessoas Juridicas em geral"),
    ),
    "empr_codi_lota_trib": (
        ("", "Selecione"),
        (1, "01 - Classificacao da atividade economica (Pessoa Juridica em Geral)"),
        (2, "02 - Obra de construcao civil - empreitada parcial ou subempreitada"),
        (3, "03 - Obra de construcao civil - empreitada total"),
        (4, "04 - Obra propria de construcao civil"),
        (5, "05 - Tomador de servicos (cessao de mao de obra)"),
        (6, "06 - Pessoa Fisica"),
        (7, "07 - Produtor Rural Pessoa Fisica"),
        (8, "08 - Operador Portuario / OGMO"),
        (9, "09 - Empregador Domestico"),
        (10, "10 - Microempreendedor Individual (MEI)"),
        (11, "11 - Segurado Especial"),
        (12, "12 - Missao Diplomatica ou Reparticao Consular"),
        (13, "13 - Entidade Beneficente de Assistencia Social"),
        (14, "14 - Orgao Publico"),
        (15, "15 - Consorcio Simplificado de Produtores Rurais"),
    ),
    "empr_simp_opta": (
        ("", "Selecione"),
        (1, "Optante"),
        (2, "Nao optante"),
    ),
    "empr_situ": (
        (1, "Normal"),
        (2, "Inativa"),
        (3, "Suspensa"),
        (4, "Encerrada"),
    ),
    "empr_indi_situ": (
        (0, "0 - Situação normal"),
        (1, "1 - Inativa"),
        (2, "2 - Suspensa"),
        (3, "3 - Encerrada"),
    ),
    "empr_tipo_caepf": (
        ("", "Selecione"),
        (1, "1 - Contribuinte Individual"),
        (2, "2 - Produtor Rural"),
        (3, "3 - Segurado Especial"),
    ),
}

LABELS = {
    "registro": "Registro",
    "empr_empr": "Código",
    "empr_fili": "Filial",
    "empr_nome": "Razão Social",
    "empr_fant": "Nome Fantasia",
    "empr_data_cada": "Data de cadastro",
    "empr_situ": "Situação",
    "empr_tipo_estab": "Tipo de estabelecimento",
    "empr_tipo_docu": "Tipo de documento",
    "empr_tipo_docu_aux": "Documento auxiliar",
    "empr_cnpj": "CNPJ",
    "empr_cpf": "CPF",
    "empr_tipo_caepf": "Tipo de CAEPF",
    "empr_caepf": "CAEPF",
    "empr_escr_muni": "Inscrição municipal",
    "empr_insc_esta": "Inscrição estadual",
    "empr_inic_ativ": "Inicio das atividades",
    "empr_fim_ativ": "Fim das atividades",
    "empr_indi_situ": "Indicativo de situação",
    "empr_capi_soci": "Capital social",
    "empr_espec_estab": "Especie do estabelecimento",
    "empr_soci_oste": "Sócio ostensivo - SCP",
    "empr_cep": "CEP",
    "empr_ende": "Endereço",
    "empr_ende_nume": "Número",
    "empr_ende_comp": "Complemento",
    "empr_ende_bair": "Bairro",
    "empr_ende_cida": "Cidade",
    "empr_ende_uf": "UF",
    "empr_ende_fone1": "Telefone",
    "empr_ende_fone2": "Telefone 2",
    "empr_ende_celu": "Celular",
    "empr_ende_emai": "E-mail",
    "empr_enqu_fede": "Enquadramento federal",
    "empr_prest_serv_anex_v_iv": "Prestadora de serviço com atividade inclusa no anexo V ou VI",
    "empr_simp_opta": "Simples",
    "empr_ativ_simp_naci": "Empresa com atividades concomitantes tributadas pelos anexos do Simples Nacional",
    "empr_cecu_ativ_simp_naci": "Centro de custo com atividades concomitantes tributadas pelos anexos do Simples Nacional",
    "empr_part_pbm": "Empresa participante do Plano Brasil Maior (PBM)",
    "empr_cecu_part_pbm": "Centro de custo participante do Plano Brasil Maior (PBM)",
    "empr_constutora": "Construtora",
    "empr_codi_paga": "Código pagamento",
    "empr_codi_paga_funrural": "Código pagamento Funrural",
    "empr_codi_paga_transp": "Código pagamento transportador",
    "empr_codi_terc": "Terceiros",
    "empr_fpas": "FPAS",
    "empr_perc_fpas": "FPAS (%)",
    "empr_class_trib": "Classificação tributária",
    "empr_codi_lota_trib": "Lotação tributária",
    "empr_cnae_prep": "CNAE Preponderante",
    "empr_cnae": "CNAE",
    "empr_perc_rat": "RAT (%)",
    "empr_perc_empregadores": "Empregadores (%)",
    "empr_perc_fap": "Alíquota FAP",
    "empr_perc_auto": "Autonomos (%)",
    "empr_rete_nf": "Retenção de nota fiscal (%)",
    "empr_perc_empregados": "Empregados (%)",
    "empr_perc_pis_folha": "% Pis folha",
    "empr_fechamento_mes": "Fechamento do mês",
    "empr_fechamento_vale_transporte": "Fechamento do vale transporte",
    "empr_tabela_inss": "Tabela de INSS",
    "empr_tabela_irrf": "Tabela de IRRF",
    "empr_tabela_irrf_plr": "Tabela de IRRF PLR",
    "empr_estouro": "Estouro",
    "empr_estouro_rescisao": "Estouro rescisão",
    "empr_etiqueta": "Etiqueta",
    "empr_ignora_faltas": "Ignora faltas nas férias",
    "empr_ignora_faltas_decimo_terceiro": "Ignora faltas no 13º",
    "empr_taxa_servico": "Taxa de serviço",
    "empr_centro_custo_departamento": "Centro de custo e departamento",
    "empr_mes_competencia_folha": "Pagamento da folha",
    "empr_calcula_ir_adiantamento_salarial": "Calcula IR no adiantamento salarial",
    "empr_ir_adiantamento_detalhado": "IR do adiantamento salarial detalhado",
    "empr_arredondamento_centavos": "Arredondamento",
    "empr_arredondamento_tipo": "Arredondar",
    "empr_grava_arredondamento_proximo_mes": "Grava arredondamento para o proximo mês",
    "empr_proporcionalidade_admissao": "Proporcionalidade admissão",
    "empr_proporcionalidade_rescisao": "Proporcionalidade rescisão",
    "empr_tipo_calculo_ferias": "Tipo de calculo para ferias",
    "empr_ferias_mensal_somente_salario": "Mensalmente somente salario (médias integral na rescisão)",
    "empr_ferias_rescisao_mes_nao_integral": "Na rescisão paga somente do mês (não integral de todos os meses)",
    "empr_ferias_paga_integral_rescisao": "Paga integralmente na rescisão (somente dias trabalhados)",
    "empr_tipo_calculo_adiantamento_13": "Tipo de cálculo para adiantamento de 13º",
    "empr_adiantamento_13_mensal_somente_salario": "Mensalmente somente salário (médias integral na rescisão)",
    "empr_adiantamento_13_rescisao_mes_nao_integral": "Na rescisão paga somente do mês (não integral de todos os meses)",
    "empr_adiantamento_13_paga_integral_rescisao": "Paga integralmente na rescisão (somente dias trabalhados)",
    "empr_ferias_coletivas_muda_periodo_aquisitivo_menos_12_meses": "Mudar periodo aquisitivo para funcionários com menos de 12 meses",
    "empr_ferias_coletivas_saldo_inferior_dias_gozo": "Saldo inferior aos dias de gozo",
    "empr_ferias_coletivas_funcionarios_mais_12_meses": "Funcionários com mais de 12 meses",
    "empr_nao_considera_faltas_horas_ferias": "Não considerar faltas horas nas férias",
    "empr_arredonda_ferias_cima": "Arredondar para cima",
    "empr_calcula_folhas_tomador": "Calcula folhas por tomador",
    "empr_nao_considera_verbas_exclusivas_tomador_principal": "Não considera verbas exclusivas para tomador principal",
    "empr_usa_centro_custo_cadastro_funcionario_13_salario": "Usar centro de custo do cadastro do funcionário no 13º salário",
    "empr_horas_apura_rateio_quadro_horarios": "Horistas - apura rateio conforme quadro de horários",
    "empr_agrupar_centros_custo_mesmo_cnpj_cei": "Agrupar centros de custo com o mesmo CNPJ/CEI",
    "empr_pagar_somente_abono_ferias": "Pagar somente abono nas férias",
    "empr_controla_pagamento_salario_familia": "Controla pagamento de salário familia",
    "empr_nao_prorroga_periodo_aquisitivo_bem": "Não prorroga período aquisitivo (BEm)",
    "empr_converter_referencia_horas": "Converter referência em horas",
    "empr_converter_referencia_horas_noturnas": "Converter referência em horas noturnas",
    "empr_converter_referencia_centesimal_planilhas": "Converter referência em centesimal na importação de planilhas",
    "empr_sindicalizada": "Sindicalizada",
    "empr_nao_lanca_compensacao_reembolso": "Não lança compensação do reembolso",
    "empr_controla_contas_bancarias_funcionarios": "Controla contas bancárias dos funcionários",
    "empr_pagar_decimo_terceiro_complementar_folha_normal": "Pagar 13º complementar na folha normal",
    "empr_pagar_decimo_terceiro_integral_bem": "Pagar 13º salário integral (BEm)",
    "empr_perc_adiantamento_salario": "% adiantamento de salário",
    "empr_primeira_declaracao_caged": "1ª declaração para Caged",
    "empr_medias": "Médias",
    "empr_mensagem_aniversario": "Mensagem de aniversário",
    "empr_prazo_experiencia": "Prazo experiencia",
    "empr_contabilizacao": "Contabilização",
    "empr_emissao_guias": "Emissão guias",
    "empr_sefip": "Sefip",
    "empr_proporcionalidade_ferias": "Proporcionalidade férias",
    "empr_proporcionalidade_situacao": "Proporcionalidade situação",
    "empr_proporcionalidade_adiantamento": "Proporcionalidade adiantamento",
    "empr_proporcionalidade_tomador": "Proporcionalidade tomador",
    "empr_verba_mensalista": "Mensalista",
    "empr_verba_mensalista_desc": "Descrição mensalista",
    "empr_verba_diarista": "Diarista",
    "empr_verba_diarista_desc": "Descrição diarista",
    "empr_verba_horista": "Horista",
    "empr_verba_horista_desc": "Descrição horista",
    "empr_verba_horista_especial": "Horista especial",
    "empr_verba_horista_especial_desc": "Descrição horista especial",
    "empr_verba_pro_labore": "Pro-labore",
    "empr_verba_pro_labore_desc": "Descrição pro-labore",
    "empr_verba_pro_labore_fgts": "Pro-labore com FGTS",
    "empr_verba_pro_labore_fgts_desc": "Descrição pro-labore com FGTS",
    "empr_verba_estagiario": "Estagiario",
    "empr_verba_estagiario_desc": "Descrição estagiario",
    "empr_verba_aposentado": "Aposentado",
    "empr_verba_aposentado_desc": "Descrição aposentado",
    "empr_verba_tarefeiro": "Tarefeiro",
    "empr_verba_tarefeiro_desc": "Descrição tarefeiro",
    "empr_verba_iss": "ISS",
    "empr_verba_iss_desc": "Descrição ISS",
    "empr_verba_contribuicao_sest": "Contribuição SEST",
    "empr_verba_contribuicao_sest_desc": "Descrição contribuição SEST",
    "empr_verba_contribuicao_senat": "Contribuição SENAT",
    "empr_verba_contribuicao_senat_desc": "Descrição contribuição SENAT",
    "empr_verba_intermitente": "Intermitente",
    "empr_verba_intermitente_desc": "Descrição intermitente",
    "empr_verba_domestica_fgts": "Domestica c/ FGTS",
    "empr_verba_domestica_fgts_desc": "Descrição de domestica c/ FGTS",
    "empr_verba_domestica_sem_fgts": "Domestica s/ FGTS",
    "empr_verba_domestica_sem_fgts_desc": "Descrição de domestica s/ FGTS",
    "empr_verba_autonomo": "Autonomo",
    "empr_verba_autonomo_desc": "Descrição de autonomo",
    "empr_verba_comissionado": "Comissionado",
    "empr_verba_comissionado_desc": "Descrição comissionado",
    "empr_verba_pagamento_semanal": "Pagamento semanal",
    "empr_verba_pagamento_semanal_desc": "Descrição pagamento semanal",
    "empr_verba_pagamento_semanal_pro": "Pagto. semanal pro",
    "empr_verba_pagamento_semanal_pro_desc": "Descrição pagto. semanal pro",
    "empr_verba_pagamento_semanal_aut": "Pagto. semanal aut.",
    "empr_verba_pagamento_semanal_aut_desc": "Descrição pagto. semanal aut.",
    "empr_verba_plr": "Verba de PLR",
    "empr_verba_plr_desc": "Descrição verba de PLR",
    "empr_verba_pagamento_quinzenal": "Pagamento quinzenal",
    "empr_verba_pagamento_quinzenal_desc": "Descrição pagamento quinzenal",
    "empr_verba_pagamento_quinzenal_pro": "Pagto. quinzenal pro",
    "empr_verba_pagamento_quinzenal_pro_desc": "Descrição pagto. quinzenal pro",
    "empr_verba_pagamento_quinzenal_aut": "Pagto. quinzenal aut.",
    "empr_verba_pagamento_quinzenal_aut_desc": "Descrição pagto. quinzenal aut.",
    "empr_verba_multa_verde_amarelo": "Multa Verde e Amarelo",
    "empr_verba_multa_verde_amarelo_desc": "Descrição multa Verde e Amarelo",
    "empr_obse": "Observações",
}

ERROR_MESSAGES = {
    "registro": {"required": "Informe o registro."},
    "empr_empr": {
        "required": "Informe a empresa.",
        "invalid": "Informe um numero valido para Código.",
    },
    "empr_fili": {
        "required": "Informe a filial.",
        "invalid": "Informe um numero valido para Filial.",
    },
    "empr_nome": {"required": "Informe a descrição."},
}


class EmpresasForm(forms.ModelForm):
    empr_cnae_prep = forms.CharField(required=False, label="CNAE PREPONDERANTE")
    empr_cnae = forms.CharField(required=False, label="CNAE")
    _cnae_validation_cache = {}

    class Meta:
        model = Empresas
        fields = ALL_FIELDS
        labels = LABELS
        error_messages = ERROR_MESSAGES

    def __init__(self, *args, banco=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.banco = (banco or "").strip()
        self._original_chave = {
            "registro": getattr(self.instance, "registro", None),
            "empr_empr": getattr(self.instance, "empr_empr", None),
            "empr_fili": getattr(self.instance, "empr_fili", None),
        }

        if self.banco and not self.initial.get("registro"):
            self.initial["registro"] = self.banco
            self.fields["registro"].initial = self.banco

        self._apply_table_reference_initials()

        for campo in ("empr_cnae_prep", "empr_cnae"):
            valor_atual = self.initial.get(campo)
            if valor_atual in (None, ""):
                valor_atual = getattr(self.instance, campo, None)
            valor_digits = _normalize_cnae_digits(valor_atual, pad_left=True)
            if valor_digits:
                descricao = self._get_cnae_description(valor_digits)
                valor_formatado = _format_cnae_display(valor_digits, descricao)
                self.initial[campo] = valor_formatado
                self.fields[campo].initial = valor_formatado

        for campo, field in self.fields.items():
            field.widget.attrs["autocomplete"] = "off"

            if isinstance(field, forms.BooleanField):
                field.required = False
                field.widget = forms.CheckboxInput(
                    attrs={"class": "form-check-input empresa-check-input"}
                )
                continue

            if campo in RADIO_CHOICES:
                field.choices = RADIO_CHOICES[campo]
                field.widget = forms.RadioSelect(
                    choices=RADIO_CHOICES[campo],
                    attrs={"class": "empresa-radio-input"},
                )
                continue

            if campo in SELECT_CHOICES:
                field.choices = SELECT_CHOICES[campo]
                field.widget = forms.Select(
                    choices=SELECT_CHOICES[campo],
                    attrs={"class": "form-select"}
                )
                if campo == "empr_situ":
                    field.initial = self.initial.get(campo) or 1
                elif campo == "empr_indi_situ":
                    field.initial = self.initial.get(campo) if self.initial.get(campo) is not None else 0
                continue

            if campo in TEXTAREA_FIELDS:
                field.widget.attrs.update({"class": "form-control", "rows": 4})
                continue

            if campo in DATE_FIELDS:
                field.widget = forms.DateInput(
                    attrs={"class": "form-control", "type": "date", "autocomplete": "off"},
                    format="%Y-%m-%d",
                )
                continue

            field.widget.attrs["class"] = "form-control"

            if campo in DECIMAL_FIELDS:
                field.widget.attrs["inputmode"] = "decimal"
            elif isinstance(field, forms.IntegerField) or campo in DIGIT_ONLY_FIELDS:
                field.widget.attrs["inputmode"] = "numeric"

            if campo in EMAIL_FIELDS:
                field.widget.attrs["type"] = "email"

        self.fields["registro"].widget = forms.HiddenInput()
        self.fields["registro"].required = False
        self.fields["empr_empr"].required = True
        self.fields["empr_fili"].required = True
        self.fields["empr_nome"].required = True
        self._configure_masked_field(
            "empr_cnpj",
            18,
            {"maxlength": "18", "placeholder": "00.000.000/0000-00", "data-mask": "cnpj"},
        )
        self._configure_masked_field(
            "empr_cpf",
            14,
            {"maxlength": "14", "placeholder": "000.000.000-00", "data-mask": "cpf"},
        )
        self._configure_masked_field(
            "empr_caepf",
            18,
            {"maxlength": "18", "placeholder": "000.000.000/0000-00", "data-mask": "caepf"},
        )
        self._configure_masked_field(
            "empr_cep",
            9,
            {"maxlength": "9", "placeholder": "00000-000", "data-mask": "cep"},
        )

        for campo in ("empr_ende_fone1", "empr_ende_fone2", "empr_ende_celu"):
            self._configure_masked_field(
                campo,
                15,
                {"maxlength": "15", "placeholder": "(00) 00000-0000", "data-mask": "phone"},
            )

        for campo in (
            "empr_tabela_inss",
            "empr_tabela_irrf",
            "empr_tabela_irrf_plr",
            "empr_primeira_declaracao_caged",
        ):
            self._configure_display_reference_field(
                campo,
                7,
                {
                    "maxlength": "7",
                    "placeholder": "MM/AAAA",
                    "inputmode": "numeric",
                    "data-mask": "month-reference",
                }
            )

    def _get_latest_reference_value(self, model_class, reference_field):
        db_alias = get_db_from_slug(self.banco)
        try:
            return (
                model_class.objects.using(db_alias)
                .order_by("-{}".format(reference_field))
                .values_list(reference_field, flat=True)
                .first()
                or ""
            )
        except Exception:
            return ""

    def _format_reference_initial_value(self, value):
        return _format_company_table_reference_display(value)

    def _apply_table_reference_initials(self):
        latest_irrf_reference = self._get_latest_reference_value(Tabelairrf, "irrf_refe")
        defaults = {
            "empr_tabela_inss": self._get_latest_reference_value(Tabelainss, "tabe_refe"),
            "empr_tabela_irrf": latest_irrf_reference,
            "empr_tabela_irrf_plr": latest_irrf_reference,
        }

        for campo in (
            "empr_tabela_inss",
            "empr_tabela_irrf",
            "empr_tabela_irrf_plr",
            "empr_primeira_declaracao_caged",
        ):
            valor_atual = self.initial.get(campo)
            if valor_atual in (None, ""):
                valor_atual = getattr(self.instance, campo, None)
            if valor_atual in (None, ""):
                valor_atual = defaults.get(campo, "")

            valor_formatado = self._format_reference_initial_value(valor_atual)
            if valor_formatado:
                self.initial[campo] = valor_formatado
                self.fields[campo].initial = valor_formatado

        for campo in ("empr_escr_muni", "empr_insc_esta"):
            self.fields[campo].widget.attrs.update({"maxlength": "25", "data-digits-only": "true"})

        for campo in ("empr_cnae_prep", "empr_cnae"):
            self.fields[campo].widget = forms.TextInput(
                attrs={
                    "class": "form-control",
                    "list": "cnae-subclasses-options",
                    "maxlength": "180",
                    "placeholder": "Digite ou selecione o CNAE",
                    "data-cnae-combobox": "true",
                }
            )

    def get_tab_errors(self):
        return {
            tab: any(self[field_name].errors for field_name in field_names)
            for tab, field_names in TAB_FIELD_GROUPS.items()
        }

    def validate_unique(self):
        registro = self.cleaned_data.get("registro") or self.banco
        empr_empr = self.cleaned_data.get("empr_empr")
        empr_fili = self.cleaned_data.get("empr_fili")

        if not registro or empr_empr in (None, "") or empr_fili in (None, ""):
            return

        db_alias = get_db_from_slug(registro)
        existe = Empresas.objects.using(db_alias).filter(
            registro=registro,
            empr_empr=empr_empr,
            empr_fili=empr_fili,
        ).exists()

        if not existe:
            return

        chave_atual = {
            "registro": registro,
            "empr_empr": empr_empr,
            "empr_fili": empr_fili,
        }

        if chave_atual == self._original_chave:
            return

        self.add_error(
            "empr_empr",
            "Ja existe uma empresa com este codigo e filial nesta licenca.",
        )

    def clean(self):
        cleaned_data = super().clean()
        registro = cleaned_data.get("registro") or self.banco
        cnpj = cleaned_data.get("empr_cnpj")
        cpf = cleaned_data.get("empr_cpf")

        if not cnpj and not cpf:
            mensagem = "Informe um CNPJ ou um CPF."
            self.add_error("empr_cnpj", mensagem)
            self.add_error("empr_cpf", mensagem)
            return cleaned_data

        if cnpj and cpf:
            mensagem = "Informe somente CNPJ ou CPF, nao os dois ao mesmo tempo."
            self.add_error("empr_cnpj", mensagem)
            self.add_error("empr_cpf", mensagem)
            return cleaned_data

        if not registro:
            return cleaned_data

        db_alias = get_db_from_slug(registro)
        chave_original = self._original_chave

        if cnpj:
            cnpj_qs = Empresas.objects.using(db_alias).filter(
                registro=registro,
                empr_cnpj=cnpj,
            )
            if EmpresasChaveService.chave_preenchida(chave_original):
                cnpj_qs = cnpj_qs.exclude(
                    registro=chave_original["registro"],
                    empr_empr=chave_original["empr_empr"],
                    empr_fili=chave_original["empr_fili"],
                )
            if cnpj_qs.exists():
                self.add_error(
                    "empr_cnpj",
                    "Ja existe outra empresa ou filial desta licenca com este CNPJ.",
                )

        if cpf:
            cpf_qs = Empresas.objects.using(db_alias).filter(
                registro=registro,
                empr_cpf=cpf,
            )
            if EmpresasChaveService.chave_preenchida(chave_original):
                cpf_qs = cpf_qs.exclude(
                    registro=chave_original["registro"],
                    empr_empr=chave_original["empr_empr"],
                    empr_fili=chave_original["empr_fili"],
                )
            if cpf_qs.exists():
                self.add_error(
                    "empr_cpf",
                    "Ja existe outra empresa ou filial desta licenca com este CPF.",
                )

        return cleaned_data

    def _configure_masked_field(self, field_name, max_length, widget_attrs):
        field = self.fields[field_name]
        field.max_length = max_length
        field.validators = [
            validator
            for validator in field.validators
            if not isinstance(validator, MaxLengthValidator)
        ]
        field.validators.append(MaxLengthValidator(max_length))
        field.widget.attrs.update(widget_attrs)

    def _configure_display_reference_field(self, field_name, max_length, widget_attrs):
        field = self.fields[field_name]
        field.max_length = max_length
        field.validators = [
            validator
            for validator in field.validators
            if not isinstance(validator, MaxLengthValidator)
        ]
        field.validators.append(MaxLengthValidator(max_length))
        field.widget.attrs.update(widget_attrs)

    def clean_registro(self):
        registro = self.banco or (self.cleaned_data.get("registro") or "").strip()
        if not registro:
            raise forms.ValidationError("Informe o registro.")
        return "".join(ch for ch in registro if ch.isdigit()) or registro

    def _calculate_mod11_digit(self, numbers, weights):
        total = sum(int(number) * weight for number, weight in zip(numbers, weights))
        remainder = total % 11
        return "0" if remainder < 2 else str(11 - remainder)

    def _is_valid_cpf(self, digits):
        if len(digits) != 11 or digits == digits[0] * 11:
            return False

        first_digit = self._calculate_mod11_digit(digits[:9], range(10, 1, -1))
        second_digit = self._calculate_mod11_digit(digits[:9] + first_digit, range(11, 1, -1))
        return digits[-2:] == first_digit + second_digit

    def _is_valid_cnpj(self, digits):
        if len(digits) != 14 or digits == digits[0] * 14:
            return False

        first_digit = self._calculate_mod11_digit(digits[:12], (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2))
        second_digit = self._calculate_mod11_digit(
            digits[:12] + first_digit,
            (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2),
        )
        return digits[-2:] == first_digit + second_digit

    def _clean_digits(self, field_name, expected_length, label):
        value = (self.cleaned_data.get(field_name) or "").strip()
        if not value:
            return value

        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) != expected_length:
            raise forms.ValidationError(f"Informe {label} com {expected_length} digitos.")
        return digits

    def _clean_digits_max(self, field_name, max_length):
        value = (self.cleaned_data.get(field_name) or "").strip()
        if not value:
            return value
        return "".join(ch for ch in value if ch.isdigit())[:max_length]

    @classmethod
    def _get_cnae_description(cls, digits):
        if not digits:
            return None

        if digits in cls._cnae_validation_cache:
            return cls._cnae_validation_cache[digits]

        descricao = None
        try:
            with urllib_request.urlopen(
                CNAE_SUBCLASSE_DETALHE_API_URL.format(codigo=digits),
                timeout=5,
            ) as response:
                data = json.loads(response.read().decode("utf-8"))
            if isinstance(data, dict):
                descricao = data.get("descricao")
        except (urllib_error.URLError, ValueError, TimeoutError):
            descricao = None

        cls._cnae_validation_cache[digits] = descricao
        return descricao

    def _clean_cnae_field(self, field_name, label, *, as_integer=False):
        value = (self.cleaned_data.get(field_name) or "").strip()
        if not value:
            return None if as_integer else ""

        digits = _normalize_cnae_digits(value, pad_left=True)
        if len(digits) != 7:
            raise forms.ValidationError("Informe um {} valido.".format(label))

        if not self._get_cnae_description(digits):
            raise forms.ValidationError("Informe um {} valido.".format(label))

        if as_integer:
            return int(digits)
        return digits

    def clean_empr_cnpj(self):
        digits = self._clean_digits("empr_cnpj", 14, "um CNPJ")
        if digits and not self._is_valid_cnpj(digits):
            raise forms.ValidationError("Informe um CNPJ valido.")
        return digits

    def clean_empr_cpf(self):
        digits = self._clean_digits("empr_cpf", 11, "um CPF")
        if digits and not self._is_valid_cpf(digits):
            raise forms.ValidationError("Informe um CPF valido.")
        return digits

    def clean_empr_caepf(self):
        return self._clean_digits("empr_caepf", 14, "um CAEPF")

    def clean_empr_cep(self):
        return self._clean_digits("empr_cep", 8, "um CEP")

    def clean_empr_escr_muni(self):
        return self._clean_digits_max("empr_escr_muni", 25)

    def clean_empr_insc_esta(self):
        return self._clean_digits_max("empr_insc_esta", 25)

    def clean_empr_ende_fone1(self):
        return self._clean_digits_max("empr_ende_fone1", 11)

    def clean_empr_ende_fone2(self):
        return self._clean_digits_max("empr_ende_fone2", 11)

    def clean_empr_ende_celu(self):
        return self._clean_digits_max("empr_ende_celu", 11)

    def clean_empr_tabela_inss(self):
        return self._clean_month_reference_field("empr_tabela_inss", "a tabela de INSS")

    def clean_empr_tabela_irrf(self):
        return self._clean_month_reference_field("empr_tabela_irrf", "a tabela de IRRF")

    def clean_empr_tabela_irrf_plr(self):
        return self._clean_month_reference_field("empr_tabela_irrf_plr", "a tabela de IRRF PLR")

    def clean_empr_primeira_declaracao_caged(self):
        return self._clean_month_reference_field(
            "empr_primeira_declaracao_caged",
            "a 1ª declaração para Caged",
        )

    def _clean_month_reference_field(self, field_name, label):
        value = (self.cleaned_data.get(field_name) or "").strip()
        if not value:
            return ""

        try:
            return _normalize_company_table_reference_storage(value)
        except ValueError:
            raise forms.ValidationError("Informe {} no formato MM/AAAA.".format(label))

    def clean_empr_cnae_prep(self):
        return self._clean_cnae_field("empr_cnae_prep", "CNAE preponderante", as_integer=True)

    def clean_empr_cnae(self):
        return self._clean_cnae_field("empr_cnae", "CNAE")
