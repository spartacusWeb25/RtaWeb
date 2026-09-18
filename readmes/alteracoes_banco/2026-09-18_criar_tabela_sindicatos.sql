-- ======================================================================
-- DDL: Criar tabela `sindicatos` (Sindicatos Trabalhadores)
-- PK COMPOSTA REAL 4 cols: (registro, sind_empr, sind_fili, sind_codi)
-- managed=False → nenhuma migration Django roda nesta tabela.
-- Total colunas: 109
-- ======================================================================

DROP TABLE IF EXISTS public.sindicatos CASCADE;

CREATE TABLE public.sindicatos (
    -- PK composta REAL multi-tenant (4 cols)
    registro character varying(14) NOT NULL,
    sind_empr integer NOT NULL,
    sind_fili integer NOT NULL,
    sind_codi integer NOT NULL,

    -- Aba 1: Cadastrais (34 cols)
    sind_nome character varying(200),
    sind_apelido character varying(100),
    sind_tipo_entidade integer,
    sind_entidade character varying(20),
    sind_codi_sind character varying(15),
    sind_agencia_grcs integer,
    sind_codi_cede character varying(15),
    sind_cep character varying(8),
    sind_logr integer,
    sind_logr_desc character varying(60),
    sind_ende character varying(120),
    sind_ende_nume character varying(20),
    sind_ende_comp character varying(60),
    sind_ende_bair character varying(60),
    sind_cida_codi integer,
    sind_cida_desc character varying(60),
    sind_esta character varying(2),
    sind_ddd1 character varying(4),
    sind_fone1 character varying(20),
    sind_ddd2 character varying(4),
    sind_fone2 character varying(20),
    sind_cnpj character varying(14),
    sind_tabela integer,
    sind_site character varying(150),
    sind_emai character varying(100),

    -- ================================================================
    -- Aba 2: DADOS VARIÁVEIS MÊS A MÊS (26 cols)
    -- ================================================================
    sind_dv_piso_salarial numeric(18,2),
    sind_dv_base_adicionais numeric(18,2),
    sind_dv_indice numeric(15,6),
    sind_dv_maior_remuneracao numeric(18,2),
    sind_dv_maior_rem_agrupada boolean,
    sind_dv_aviso_previo_2anos boolean,
    sind_dv_perc_abono_ferias numeric(8,2),
    sind_dv_abono_sigla character varying(3),
    sind_dv_meses_ferias_dobro integer,
    sind_dv_meses_ferias_justa integer,
    sind_dv_ferias_rescisao integer,
    sind_dv_perc_adicional_noturno numeric(8,2),
    sind_dv_data_base_mes integer,
    sind_dv_estabilidade_dias integer,
    sind_dv_liminar_aviso_codi integer,
    sind_dv_liminar_aviso_13 boolean,
    sind_dv_verba_multa_codi integer,
    sind_dv_verba_multa_desc character varying(120),
    sind_dv_mes_desc_sindical integer,
    sind_dv_meses_homologacao integer,
    sind_dv_mes_contribuicao_opcao integer,
    sind_dv_hora_noturna_inicio character varying(5),
    sind_dv_hora_noturna_fim character varying(5),
    sind_dv_pagar_13_integral_bem boolean,
    sind_dv_nao_prorroga_aquisitivo_bem boolean,

    -- ================================================================
    -- Aba 3: MÉDIAS (49 cols)
    -- ================================================================
    -- Checkboxes topo
    sind_md_calc_maiores_meses_verba boolean,
    sind_md_calc_proporcional_verba boolean,

    -- Médias para situação (3 linhas × 6 cols = 18)
    sind_md_sit_rv_mes1 integer,
    sind_md_sit_rv_mes2 integer,
    sind_md_sit_rv_val1 numeric(12,2),
    sind_md_sit_rv_val2 numeric(12,2),
    sind_md_sit_rv_val3 numeric(12,2),
    sind_md_sit_rv_val4 numeric(12,2),

    sind_md_sit_he_mes1 integer,
    sind_md_sit_he_mes2 integer,
    sind_md_sit_he_val1 numeric(12,2),
    sind_md_sit_he_val2 numeric(12,2),
    sind_md_sit_he_val3 numeric(12,2),
    sind_md_sit_he_val4 numeric(12,2),

    sind_md_sit_hn_mes1 integer,
    sind_md_sit_hn_mes2 integer,
    sind_md_sit_hn_val1 numeric(12,2),
    sind_md_sit_hn_val2 numeric(12,2),
    sind_md_sit_hn_val3 numeric(12,2),
    sind_md_sit_hn_val4 numeric(12,2),

    -- Médias para férias + 13º (3 linhas × 6 + 2 check = 20)
    sind_md_fer_rv_mes1 integer,
    sind_md_fer_rv_mes2 integer,
    sind_md_fer_rv_val1 numeric(12,2),
    sind_md_fer_rv_val2 numeric(12,2),
    sind_md_fer_rv_val3 numeric(12,2),
    sind_md_fer_rv_val4 numeric(12,2),

    sind_md_fer_he_mes1 integer,
    sind_md_fer_he_mes2 integer,
    sind_md_fer_he_val1 numeric(12,2),
    sind_md_fer_he_val2 numeric(12,2),
    sind_md_fer_he_val3 numeric(12,2),
    sind_md_fer_he_val4 numeric(12,2),

    sind_md_fer_hn_mes1 integer,
    sind_md_fer_hn_mes2 integer,
    sind_md_fer_hn_val1 numeric(12,2),
    sind_md_fer_hn_val2 numeric(12,2),
    sind_md_fer_hn_val3 numeric(12,2),
    sind_md_fer_hn_val4 numeric(12,2),

    sind_md_fer_calc13_anterior boolean,
    sind_md_fer_calc_112_indeniz boolean,

    -- Ignorar meses zerados (3 cols)
    sind_md_ign_rv boolean,
    sind_md_ign_he boolean,
    sind_md_ign_hn boolean,

    -- Selects inferiores + checkbox (7 cols)
    sind_md_maiores_meses_opcao integer,
    sind_md_maiores_meses_desc character varying(120),
    sind_md_media_ferias_codi integer,
    sind_md_media_ferias_desc character varying(200),
    sind_md_media_ultimos_codi integer,
    sind_md_media_ultimos_desc character varying(200),
    sind_md_incluir_mes_atual boolean,

    -- Logs
    _log_data date,
    _log_time time without time zone,

    CONSTRAINT pk_sindicatos PRIMARY KEY (registro, sind_empr, sind_fili, sind_codi)
);

ALTER TABLE public.sindicatos OWNER TO postgres;

-- Índices de performance
CREATE INDEX idx_sindicatos_busca_nome ON public.sindicatos (registro, sind_nome);
CREATE INDEX idx_sindicatos_cnpj ON public.sindicatos (registro, sind_cnpj);
CREATE INDEX idx_sindicatos_codigo ON public.sindicatos (registro, sind_empr, sind_fili, sind_codi);
