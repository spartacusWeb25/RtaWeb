-- Estrutura base da tabela public.empresas

BEGIN;

DROP TABLE IF EXISTS public.empresas;

CREATE TABLE public.empresas (
    -- Chave primaria composta
    registro varchar(14) NOT NULL,
    empr_empr integer NOT NULL,
    empr_fili integer NOT NULL,

    -- aba Cadastrais
    empr_nome varchar(200) NOT NULL,
    empr_fant varchar(200),
    empr_data_cada date,
    empr_situ integer,
    empr_tipo_estab integer,
    empr_tipo_docu integer,
    empr_tipo_docu_aux integer,
    empr_cnpj varchar(14),
    empr_cpf varchar(11),
    empr_tipo_caepf integer,
    empr_caepf varchar(14),
    empr_escr_muni varchar(25),
    empr_insc_esta varchar(25),
    empr_inic_ativ date,
    empr_fim_ativ date,
    empr_indi_situ integer,
    empr_capi_soci numeric(15,2),
    empr_espec_estab varchar(60),
    empr_soci_oste boolean,

    -- aba Endereco
    empr_cep varchar(8),
    empr_logr integer,
    empr_ende varchar(120),
    empr_ende_nume varchar(20),
    empr_ende_comp varchar(60),
    empr_ende_bair varchar(60),
    empr_ende_cida varchar(60),
    empr_ende_uf varchar(2),
    empr_ende_fone1 varchar(14),
    empr_ende_fone2 varchar(14),
    empr_ende_celu varchar(14),
    empr_ende_emai varchar(200),

    -- aba GPS / Tributacao
    empr_enqu_fede integer,
    empr_prest_serv_anex_v_iv integer,
    empr_simp_opta integer,
    empr_ativ_simp_naci boolean,
    empr_cecu_ativ_simp_naci boolean,
    empr_part_pbm boolean,
    empr_cecu_part_pbm boolean,
    empr_constutora boolean,
    empr_codi_paga integer,
    empr_codi_paga_funrural integer,
    empr_codi_paga_transp integer,
    empr_codi_terc integer,
    empr_fpas integer,
    empr_perc_fpas numeric(5,2),
    empr_class_trib integer,
    empr_codi_lota_trib integer,
    empr_cnae_prep integer,
    empr_cnae varchar(10),
    empr_perc_rat numeric(5,2),
    empr_perc_empregadores numeric(5,2),
    empr_perc_fap numeric(5,2),
    empr_perc_auto numeric(5,2),
    empr_rete_nf numeric(5,2),
    empr_perc_empregados numeric(5,2),

    -- aba Parametros Gerais 1
    empr_perc_pis_folha numeric(5,2),
    empr_fechamento_mes integer,
    empr_fechamento_vale_transporte integer,
    empr_tabela_inss varchar(6),
    empr_tabela_irrf varchar(6),
    empr_tabela_irrf_plr varchar(6),
    empr_estouro boolean,
    empr_estouro_rescisao boolean,
    empr_etiqueta boolean,
    empr_ignora_faltas boolean,
    empr_ignora_faltas_decimo_terceiro boolean,
    empr_taxa_servico numeric(10,2),
    empr_centro_custo_departamento boolean,
    empr_mes_competencia_folha integer,
    empr_calcula_ir_adiantamento_salarial boolean,
    empr_ir_adiantamento_detalhado boolean,
    empr_arredondamento_centavos integer,
    empr_arredondamento_tipo integer,
    empr_grava_arredondamento_proximo_mes boolean,
    empr_proporcionalidade_admissao integer,
    empr_proporcionalidade_rescisao integer,
    empr_tipo_calculo_ferias integer,
    empr_ferias_mensal_somente_salario boolean,
    empr_ferias_rescisao_mes_nao_integral boolean,
    empr_ferias_paga_integral_rescisao boolean,
    empr_tipo_calculo_adiantamento_13 integer,
    empr_adiantamento_13_mensal_somente_salario boolean,
    empr_adiantamento_13_rescisao_mes_nao_integral boolean,
    empr_adiantamento_13_paga_integral_rescisao boolean,

    -- aba Parametros Gerais 2
    empr_ferias_coletivas_muda_periodo_aquisitivo_menos_12_meses boolean,
    empr_ferias_coletivas_saldo_inferior_dias_gozo integer,
    empr_ferias_coletivas_funcionarios_mais_12_meses integer,
    empr_nao_considera_faltas_horas_ferias boolean,
    empr_arredonda_ferias_cima boolean,
    empr_calcula_folhas_tomador boolean,
    empr_nao_considera_verbas_exclusivas_tomador_principal boolean,
    empr_usa_centro_custo_cadastro_funcionario_13_salario boolean,
    empr_horas_apura_rateio_quadro_horarios boolean,
    empr_agrupar_centros_custo_mesmo_cnpj_cei boolean,
    empr_pagar_somente_abono_ferias boolean,
    empr_controla_pagamento_salario_familia boolean,
    empr_nao_prorroga_periodo_aquisitivo_bem boolean,
    empr_converter_referencia_horas boolean,
    empr_converter_referencia_horas_noturnas boolean,
    empr_converter_referencia_centesimal_planilhas boolean,
    empr_sindicalizada boolean,
    empr_nao_lanca_compensacao_reembolso boolean,
    empr_controla_contas_bancarias_funcionarios boolean,
    empr_pagar_decimo_terceiro_complementar_folha_normal boolean,
    empr_pagar_decimo_terceiro_integral_bem boolean,
    empr_perc_adiantamento_salario numeric(5,2),
    empr_primeira_declaracao_caged varchar(10),
    empr_medias integer,
    empr_mensagem_aniversario integer,
    empr_prazo_experiencia integer,
    empr_contabilizacao integer,
    empr_emissao_guias integer,
    empr_sefip integer,
    empr_proporcionalidade_ferias integer,
    empr_proporcionalidade_situacao integer,
    empr_proporcionalidade_adiantamento integer,
    empr_proporcionalidade_tomador integer,

    -- aba Verbas
    empr_verba_mensalista integer,
    empr_verba_mensalista_desc varchar(120),
    empr_verba_diarista integer,
    empr_verba_diarista_desc varchar(120),
    empr_verba_horista integer,
    empr_verba_horista_desc varchar(120),
    empr_verba_horista_especial integer,
    empr_verba_horista_especial_desc varchar(120),
    empr_verba_pro_labore integer,
    empr_verba_pro_labore_desc varchar(120),
    empr_verba_pro_labore_fgts integer,
    empr_verba_pro_labore_fgts_desc varchar(120),
    empr_verba_estagiario integer,
    empr_verba_estagiario_desc varchar(120),
    empr_verba_aposentado integer,
    empr_verba_aposentado_desc varchar(120),
    empr_verba_tarefeiro integer,
    empr_verba_tarefeiro_desc varchar(120),
    empr_verba_iss integer,
    empr_verba_iss_desc varchar(120),
    empr_verba_contribuicao_sest integer,
    empr_verba_contribuicao_sest_desc varchar(120),
    empr_verba_contribuicao_senat integer,
    empr_verba_contribuicao_senat_desc varchar(120),
    empr_verba_intermitente integer,
    empr_verba_intermitente_desc varchar(120),
    empr_verba_domestica_fgts integer,
    empr_verba_domestica_fgts_desc varchar(120),
    empr_verba_domestica_sem_fgts integer,
    empr_verba_domestica_sem_fgts_desc varchar(120),
    empr_verba_autonomo integer,
    empr_verba_autonomo_desc varchar(120),
    empr_verba_comissionado integer,
    empr_verba_comissionado_desc varchar(120),
    empr_verba_pagamento_semanal integer,
    empr_verba_pagamento_semanal_desc varchar(120),
    empr_verba_pagamento_semanal_pro integer,
    empr_verba_pagamento_semanal_pro_desc varchar(120),
    empr_verba_pagamento_semanal_aut integer,
    empr_verba_pagamento_semanal_aut_desc varchar(120),
    empr_verba_plr integer,
    empr_verba_plr_desc varchar(120),
    empr_verba_pagamento_quinzenal integer,
    empr_verba_pagamento_quinzenal_desc varchar(120),
    empr_verba_pagamento_quinzenal_pro integer,
    empr_verba_pagamento_quinzenal_pro_desc varchar(120),
    empr_verba_pagamento_quinzenal_aut integer,
    empr_verba_pagamento_quinzenal_aut_desc varchar(120),
    empr_verba_multa_verde_amarelo integer,
    empr_verba_multa_verde_amarelo_desc varchar(120),

    -- aba Observacoes
    empr_obse text,

    CONSTRAINT empresas_pkey PRIMARY KEY (registro, empr_empr, empr_fili)
);

COMMENT ON TABLE public.empresas IS
'Tabela de empresas.';

COMMENT ON COLUMN public.empresas.registro IS 'Registro da licenca.';
COMMENT ON COLUMN public.empresas.empr_empr IS 'Codigo da empresa.';
COMMENT ON COLUMN public.empresas.empr_fili IS 'Filial da empresa.';
COMMENT ON COLUMN public.empresas.empr_nome IS 'Descricao da empresa.';
COMMENT ON COLUMN public.empresas.empr_fant IS 'Apelido da empresa.';
COMMENT ON COLUMN public.empresas.empr_data_cada IS 'Data de cadastro.';
COMMENT ON COLUMN public.empresas.empr_situ IS 'Situacao.';
COMMENT ON COLUMN public.empresas.empr_tipo_estab IS 'Tipo de estabelecimento.';
COMMENT ON COLUMN public.empresas.empr_tipo_docu IS 'Tipo de documento.';
COMMENT ON COLUMN public.empresas.empr_tipo_docu_aux IS 'Documento auxiliar.';
COMMENT ON COLUMN public.empresas.empr_cnpj IS 'CNPJ.';
COMMENT ON COLUMN public.empresas.empr_cpf IS 'CPF.';
COMMENT ON COLUMN public.empresas.empr_tipo_caepf IS 'Tipo de CAEPF.';
COMMENT ON COLUMN public.empresas.empr_caepf IS 'CAEPF.';
COMMENT ON COLUMN public.empresas.empr_escr_muni IS 'Inscricao municipal.';
COMMENT ON COLUMN public.empresas.empr_insc_esta IS 'Inscricao estadual.';
COMMENT ON COLUMN public.empresas.empr_inic_ativ IS 'Inicio das atividades.';
COMMENT ON COLUMN public.empresas.empr_fim_ativ IS 'Fim das atividades.';
COMMENT ON COLUMN public.empresas.empr_indi_situ IS 'Indicativo de situacao.';
COMMENT ON COLUMN public.empresas.empr_capi_soci IS 'Capital social.';
COMMENT ON COLUMN public.empresas.empr_espec_estab IS 'Especie do estabelecimento.';
COMMENT ON COLUMN public.empresas.empr_soci_oste IS 'Socio ostensivo - SCP.';

COMMENT ON COLUMN public.empresas.empr_cep IS 'CEP.';
COMMENT ON COLUMN public.empresas.empr_logr IS 'Logradouro.';
COMMENT ON COLUMN public.empresas.empr_ende IS 'Endereco.';
COMMENT ON COLUMN public.empresas.empr_ende_nume IS 'Numero.';
COMMENT ON COLUMN public.empresas.empr_ende_comp IS 'Complemento.';
COMMENT ON COLUMN public.empresas.empr_ende_bair IS 'Bairro.';
COMMENT ON COLUMN public.empresas.empr_ende_cida IS 'Cidade.';
COMMENT ON COLUMN public.empresas.empr_ende_uf IS 'UF.';
COMMENT ON COLUMN public.empresas.empr_ende_fone1 IS 'Telefone.';
COMMENT ON COLUMN public.empresas.empr_ende_fone2 IS 'Telefone 2.';
COMMENT ON COLUMN public.empresas.empr_ende_celu IS 'Celular.';
COMMENT ON COLUMN public.empresas.empr_ende_emai IS 'E-mail.';

COMMENT ON COLUMN public.empresas.empr_enqu_fede IS 'Enquadramento federal.';
COMMENT ON COLUMN public.empresas.empr_prest_serv_anex_v_iv IS 'Prestadora de servico com atividade inclusa no anexo V ou VI.';
COMMENT ON COLUMN public.empresas.empr_simp_opta IS 'Simples.';
COMMENT ON COLUMN public.empresas.empr_ativ_simp_naci IS 'Empresa com atividades concomitantes tributadas pelos anexos do Simples Nacional.';
COMMENT ON COLUMN public.empresas.empr_cecu_ativ_simp_naci IS 'Centro de custo com atividades concomitantes tributadas pelos anexos do Simples Nacional.';
COMMENT ON COLUMN public.empresas.empr_part_pbm IS 'Empresa participante do Plano Brasil Maior.';
COMMENT ON COLUMN public.empresas.empr_cecu_part_pbm IS 'Centro de custo participante do Plano Brasil Maior.';
COMMENT ON COLUMN public.empresas.empr_constutora IS 'Construtora.';
COMMENT ON COLUMN public.empresas.empr_codi_paga IS 'Codigo pagamento.';
COMMENT ON COLUMN public.empresas.empr_codi_paga_funrural IS 'Codigo pagamento Funrural.';
COMMENT ON COLUMN public.empresas.empr_codi_paga_transp IS 'Codigo pagamento transportador.';
COMMENT ON COLUMN public.empresas.empr_codi_terc IS 'Terceiros.';
COMMENT ON COLUMN public.empresas.empr_fpas IS 'FPAS.';
COMMENT ON COLUMN public.empresas.empr_perc_fpas IS 'FPAS em percentual.';
COMMENT ON COLUMN public.empresas.empr_class_trib IS 'Classificacao tributaria.';
COMMENT ON COLUMN public.empresas.empr_codi_lota_trib IS 'Lotacao tributaria.';
COMMENT ON COLUMN public.empresas.empr_cnae_prep IS 'CNAE preponderante.';
COMMENT ON COLUMN public.empresas.empr_cnae IS 'CNAE.';
COMMENT ON COLUMN public.empresas.empr_perc_rat IS 'RAT em percentual.';
COMMENT ON COLUMN public.empresas.empr_perc_empregadores IS 'Empregadores em percentual.';
COMMENT ON COLUMN public.empresas.empr_perc_fap IS 'Aliquota FAP.';
COMMENT ON COLUMN public.empresas.empr_perc_auto IS 'Autonomos em percentual.';
COMMENT ON COLUMN public.empresas.empr_rete_nf IS 'Retencao de nota fiscal em percentual.';
COMMENT ON COLUMN public.empresas.empr_perc_empregados IS 'Empregados em percentual.';

COMMENT ON COLUMN public.empresas.empr_perc_pis_folha IS 'Percentual de PIS folha.';
COMMENT ON COLUMN public.empresas.empr_fechamento_mes IS 'Fechamento do mes.';
COMMENT ON COLUMN public.empresas.empr_fechamento_vale_transporte IS 'Fechamento do vale transporte.';
COMMENT ON COLUMN public.empresas.empr_tabela_inss IS 'Tabela de INSS.';
COMMENT ON COLUMN public.empresas.empr_tabela_irrf IS 'Tabela de IRRF.';
COMMENT ON COLUMN public.empresas.empr_tabela_irrf_plr IS 'Tabela de IRRF PLR.';
COMMENT ON COLUMN public.empresas.empr_estouro IS 'Estouro.';
COMMENT ON COLUMN public.empresas.empr_estouro_rescisao IS 'Estouro rescisao.';
COMMENT ON COLUMN public.empresas.empr_etiqueta IS 'Etiqueta.';
COMMENT ON COLUMN public.empresas.empr_ignora_faltas IS 'Ignora faltas.';
COMMENT ON COLUMN public.empresas.empr_ignora_faltas_decimo_terceiro IS 'Ignora faltas no 13o.';
COMMENT ON COLUMN public.empresas.empr_taxa_servico IS 'Taxa de servico.';
COMMENT ON COLUMN public.empresas.empr_centro_custo_departamento IS 'Centro de custo e departamento.';
COMMENT ON COLUMN public.empresas.empr_mes_competencia_folha IS 'Mes da competencia da folha.';
COMMENT ON COLUMN public.empresas.empr_calcula_ir_adiantamento_salarial IS 'Calcula IR no adiantamento salarial.';
COMMENT ON COLUMN public.empresas.empr_ir_adiantamento_detalhado IS 'IR do adiantamento salarial detalhado.';
COMMENT ON COLUMN public.empresas.empr_arredondamento_centavos IS 'Arredondamento em centavos.';
COMMENT ON COLUMN public.empresas.empr_arredondamento_tipo IS 'Tipo de arredondamento.';
COMMENT ON COLUMN public.empresas.empr_grava_arredondamento_proximo_mes IS 'Grava arredondamento para o proximo mes.';
COMMENT ON COLUMN public.empresas.empr_proporcionalidade_admissao IS 'Proporcionalidade admissao.';
COMMENT ON COLUMN public.empresas.empr_proporcionalidade_rescisao IS 'Proporcionalidade rescisao.';
COMMENT ON COLUMN public.empresas.empr_tipo_calculo_ferias IS 'Tipo de calculo para ferias.';
COMMENT ON COLUMN public.empresas.empr_ferias_mensal_somente_salario IS 'Mensalmente somente salario nas ferias.';
COMMENT ON COLUMN public.empresas.empr_ferias_rescisao_mes_nao_integral IS 'Na rescisao paga somente do mes.';
COMMENT ON COLUMN public.empresas.empr_ferias_paga_integral_rescisao IS 'Paga integralmente na rescisao.';
COMMENT ON COLUMN public.empresas.empr_tipo_calculo_adiantamento_13 IS 'Tipo de calculo para adiantamento de 13o.';
COMMENT ON COLUMN public.empresas.empr_adiantamento_13_mensal_somente_salario IS 'Mensalmente somente salario no adiantamento de 13o.';
COMMENT ON COLUMN public.empresas.empr_adiantamento_13_rescisao_mes_nao_integral IS 'Na rescisao paga somente do mes no adiantamento de 13o.';
COMMENT ON COLUMN public.empresas.empr_adiantamento_13_paga_integral_rescisao IS 'Paga integralmente na rescisao no adiantamento de 13o.';

COMMENT ON COLUMN public.empresas.empr_ferias_coletivas_muda_periodo_aquisitivo_menos_12_meses IS 'Mudar periodo aquisitivo para funcionarios com menos de 12 meses.';
COMMENT ON COLUMN public.empresas.empr_ferias_coletivas_saldo_inferior_dias_gozo IS 'Ferias coletivas para saldo inferior aos dias de gozo.';
COMMENT ON COLUMN public.empresas.empr_ferias_coletivas_funcionarios_mais_12_meses IS 'Ferias coletivas para funcionarios com mais de 12 meses.';
COMMENT ON COLUMN public.empresas.empr_nao_considera_faltas_horas_ferias IS 'Nao considerar faltas e horas nas ferias.';
COMMENT ON COLUMN public.empresas.empr_arredonda_ferias_cima IS 'Arredondar para cima.';
COMMENT ON COLUMN public.empresas.empr_calcula_folhas_tomador IS 'Calcula folhas por tomador.';
COMMENT ON COLUMN public.empresas.empr_nao_considera_verbas_exclusivas_tomador_principal IS 'Nao considera verbas exclusivas para tomador principal.';
COMMENT ON COLUMN public.empresas.empr_usa_centro_custo_cadastro_funcionario_13_salario IS 'Usar centro de custo do cadastro do funcionario em 13o salario.';
COMMENT ON COLUMN public.empresas.empr_horas_apura_rateio_quadro_horarios IS 'Horas - apura rateio conforme quadro de horarios.';
COMMENT ON COLUMN public.empresas.empr_agrupar_centros_custo_mesmo_cnpj_cei IS 'Agrupar centros de custo com o mesmo CNPJ ou CEI.';
COMMENT ON COLUMN public.empresas.empr_pagar_somente_abono_ferias IS 'Pagar somente abono nas ferias.';
COMMENT ON COLUMN public.empresas.empr_controla_pagamento_salario_familia IS 'Controla pagamento de salario familia.';
COMMENT ON COLUMN public.empresas.empr_nao_prorroga_periodo_aquisitivo_bem IS 'Nao prorroga periodo aquisitivo.';
COMMENT ON COLUMN public.empresas.empr_converter_referencia_horas IS 'Converter referencia em horas.';
COMMENT ON COLUMN public.empresas.empr_converter_referencia_horas_noturnas IS 'Converter referencia em horas noturnas.';
COMMENT ON COLUMN public.empresas.empr_converter_referencia_centesimal_planilhas IS 'Converter referencia em centesimal na importacao de planilhas.';
COMMENT ON COLUMN public.empresas.empr_variacao_causada IS 'Variacao causada.';
COMMENT ON COLUMN public.empresas.empr_nao_lanca_compensacao_reembolso IS 'Nao lanca compensacao do reembolso.';
COMMENT ON COLUMN public.empresas.empr_controla_contas_bancarias_funcionarios IS 'Controla contas bancarias dos funcionarios.';
COMMENT ON COLUMN public.empresas.empr_pagar_decimo_terceiro_complementar_folha_normal IS 'Pagar 13o complementar na folha normal.';
COMMENT ON COLUMN public.empresas.empr_pagar_decimo_terceiro_integral_bem IS 'Pagar 13o salario integral.';
COMMENT ON COLUMN public.empresas.empr_perc_adiantamento_salario IS 'Percentual de adiantamento de salario.';
COMMENT ON COLUMN public.empresas.empr_primeira_declaracao_caged IS 'Primeira declaracao para Caged.';
COMMENT ON COLUMN public.empresas.empr_medias IS 'Medias.';
COMMENT ON COLUMN public.empresas.empr_mensagem_aniversario IS 'Mensagem de aniversario.';
COMMENT ON COLUMN public.empresas.empr_prazo_experiencia IS 'Prazo de experiencia.';
COMMENT ON COLUMN public.empresas.empr_contabilizacao IS 'Contabilizacao.';
COMMENT ON COLUMN public.empresas.empr_emissao_guias IS 'Emissao de guias.';
COMMENT ON COLUMN public.empresas.empr_sefip IS 'Sefip.';
COMMENT ON COLUMN public.empresas.empr_proporcionalidade_ferias IS 'Proporcionalidade de ferias.';
COMMENT ON COLUMN public.empresas.empr_proporcionalidade_situacao IS 'Proporcionalidade de situacao.';
COMMENT ON COLUMN public.empresas.empr_proporcionalidade_adiantamento IS 'Proporcionalidade de adiantamento.';
COMMENT ON COLUMN public.empresas.empr_proporcionalidade_tomador IS 'Proporcionalidade de tomador.';

COMMENT ON COLUMN public.empresas.empr_verba_mensalista IS 'Codigo da verba mensalista.';
COMMENT ON COLUMN public.empresas.empr_verba_mensalista_desc IS 'Descricao da verba mensalista.';
COMMENT ON COLUMN public.empresas.empr_verba_diarista IS 'Codigo da verba diarista.';
COMMENT ON COLUMN public.empresas.empr_verba_diarista_desc IS 'Descricao da verba diarista.';
COMMENT ON COLUMN public.empresas.empr_verba_horista IS 'Codigo da verba horista.';
COMMENT ON COLUMN public.empresas.empr_verba_horista_desc IS 'Descricao da verba horista.';
COMMENT ON COLUMN public.empresas.empr_verba_horista_especial IS 'Codigo da verba horista especial.';
COMMENT ON COLUMN public.empresas.empr_verba_horista_especial_desc IS 'Descricao da verba horista especial.';
COMMENT ON COLUMN public.empresas.empr_verba_pro_labore IS 'Codigo da verba pro-labore.';
COMMENT ON COLUMN public.empresas.empr_verba_pro_labore_desc IS 'Descricao da verba pro-labore.';
COMMENT ON COLUMN public.empresas.empr_verba_pro_labore_fgts IS 'Codigo da verba pro-labore com FGTS.';
COMMENT ON COLUMN public.empresas.empr_verba_pro_labore_fgts_desc IS 'Descricao da verba pro-labore com FGTS.';
COMMENT ON COLUMN public.empresas.empr_verba_estagiario IS 'Codigo da verba estagiario.';
COMMENT ON COLUMN public.empresas.empr_verba_estagiario_desc IS 'Descricao da verba estagiario.';
COMMENT ON COLUMN public.empresas.empr_verba_aposentado IS 'Codigo da verba aposentado.';
COMMENT ON COLUMN public.empresas.empr_verba_aposentado_desc IS 'Descricao da verba aposentado.';
COMMENT ON COLUMN public.empresas.empr_verba_tarefeiro IS 'Codigo da verba tarefeiro.';
COMMENT ON COLUMN public.empresas.empr_verba_tarefeiro_desc IS 'Descricao da verba tarefeiro.';
COMMENT ON COLUMN public.empresas.empr_verba_iss IS 'Codigo da verba ISS.';
COMMENT ON COLUMN public.empresas.empr_verba_iss_desc IS 'Descricao da verba ISS.';
COMMENT ON COLUMN public.empresas.empr_verba_contribuicao_sest IS 'Codigo da verba contribuicao SEST.';
COMMENT ON COLUMN public.empresas.empr_verba_contribuicao_sest_desc IS 'Descricao da verba contribuicao SEST.';
COMMENT ON COLUMN public.empresas.empr_verba_contribuicao_senat IS 'Codigo da verba contribuicao SENAT.';
COMMENT ON COLUMN public.empresas.empr_verba_contribuicao_senat_desc IS 'Descricao da verba contribuicao SENAT.';
COMMENT ON COLUMN public.empresas.empr_verba_intermitente IS 'Codigo da verba intermitente.';
COMMENT ON COLUMN public.empresas.empr_verba_intermitente_desc IS 'Descricao da verba intermitente.';
COMMENT ON COLUMN public.empresas.empr_verba_domestica_fgts IS 'Codigo da verba domestica com FGTS.';
COMMENT ON COLUMN public.empresas.empr_verba_domestica_fgts_desc IS 'Descricao da verba domestica com FGTS.';
COMMENT ON COLUMN public.empresas.empr_verba_domestica_sem_fgts IS 'Codigo da verba domestica sem FGTS.';
COMMENT ON COLUMN public.empresas.empr_verba_domestica_sem_fgts_desc IS 'Descricao da verba domestica sem FGTS.';
COMMENT ON COLUMN public.empresas.empr_verba_autonomo IS 'Codigo da verba autonomo.';
COMMENT ON COLUMN public.empresas.empr_verba_autonomo_desc IS 'Descricao da verba autonomo.';
COMMENT ON COLUMN public.empresas.empr_verba_comissionado IS 'Codigo da verba comissionado.';
COMMENT ON COLUMN public.empresas.empr_verba_comissionado_desc IS 'Descricao da verba comissionado.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_semanal IS 'Codigo da verba pagamento semanal.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_semanal_desc IS 'Descricao da verba pagamento semanal.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_semanal_pro IS 'Codigo da verba pagamento semanal pro.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_semanal_pro_desc IS 'Descricao da verba pagamento semanal pro.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_semanal_aut IS 'Codigo da verba pagamento semanal autonomo.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_semanal_aut_desc IS 'Descricao da verba pagamento semanal autonomo.';
COMMENT ON COLUMN public.empresas.empr_verba_plr IS 'Codigo da verba de PLR.';
COMMENT ON COLUMN public.empresas.empr_verba_plr_desc IS 'Descricao da verba de PLR.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_quinzenal IS 'Codigo da verba pagamento quinzenal.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_quinzenal_desc IS 'Descricao da verba pagamento quinzenal.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_quinzenal_pro IS 'Codigo da verba pagamento quinzenal pro.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_quinzenal_pro_desc IS 'Descricao da verba pagamento quinzenal pro.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_quinzenal_aut IS 'Codigo da verba pagamento quinzenal autonomo.';
COMMENT ON COLUMN public.empresas.empr_verba_pagamento_quinzenal_aut_desc IS 'Descricao da verba pagamento quinzenal autonomo.';
COMMENT ON COLUMN public.empresas.empr_verba_multa_verde_amarelo IS 'Codigo da verba multa verde e amarelo.';
COMMENT ON COLUMN public.empresas.empr_verba_multa_verde_amarelo_desc IS 'Descricao da verba multa verde e amarelo.';

COMMENT ON COLUMN public.empresas.empr_obse IS 'Observacoes.';

COMMIT;
