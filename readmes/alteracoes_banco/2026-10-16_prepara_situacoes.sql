CREATE TABLE IF NOT EXISTS public.prepara_situacoes (
    registro character varying(14) NOT NULL,
    prep_empr integer NOT NULL,
    prep_fili integer NOT NULL,
    prep_codi integer NOT NULL,
    prep_desc character varying(200) DEFAULT ''::character varying,
    prep_descricao character varying(250) DEFAULT ''::character varying,
    prep_situacao_fixa boolean DEFAULT false,
    prep_desc_situacao_folha boolean DEFAULT false,
    prep_calcula_salario_familia boolean DEFAULT false,
    prep_13_integral boolean DEFAULT false,
    prep_reembolso_gps_13 boolean DEFAULT false,
    prep_prorroga_periodo_aquisitivo boolean DEFAULT false,
    prep_meses_media_sindicato boolean DEFAULT false,
    prep_desc_tempo_servico boolean DEFAULT false,
    prep_nao_prorroga_ult_prazo_ferias boolean DEFAULT false,
    prep_perde_pa_afast_super_30 boolean DEFAULT false,
    prep_ignora_inss_13 boolean DEFAULT false,
    prep_ignora_ir_13 boolean DEFAULT false,
    prep_ignora_fgts_13 boolean DEFAULT false,
    prep_grupo_situacao character varying(120) DEFAULT ''::character varying,
    prep_usuario_inc character varying(30),
    prep_data_inc date,
    prep_usuario_alt character varying(30),
    prep_data_alt date,
    CONSTRAINT prepara_situacoes_pk PRIMARY KEY (registro, prep_empr, prep_fili, prep_codi)
);

CREATE INDEX IF NOT EXISTS prepara_situacoes_idx1
    ON public.prepara_situacoes (registro, prep_empr, prep_fili);
