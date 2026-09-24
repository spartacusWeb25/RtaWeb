-- ============================================================================
-- DDL: Nova tabela public.departamentosrh (PK Composta multi-tenant 4 colunas)
-- Apagar a tabela antiga se existir (DROP), depois rodar este script no Postgres
-- ============================================================================

DROP TABLE IF EXISTS public.departamentosrh;

CREATE TABLE IF NOT EXISTS public.departamentosrh (
    -- ===============================================================
    -- PK COMPOSTA REAL 4 colunas (igual todos os outros apps legados)
    -- ===============================================================
    registro          VARCHAR(14)   NOT NULL,
    depa_empr         INTEGER       NOT NULL DEFAULT 1,
    depa_fili         INTEGER       NOT NULL DEFAULT 1,
    depa_codi         INTEGER       NOT NULL,

    -- ===============================================================
    -- ABA 1: CADASTRAIS (básicos)
    -- ===============================================================
    depa_desc         VARCHAR(200)  NOT NULL DEFAULT '',
    depa_apelido      VARCHAR(100)       NULL DEFAULT NULL,
    depa_inativo      BOOLEAN       NOT NULL DEFAULT FALSE,

    -- Endereço
    depa_cep          VARCHAR(8)         NULL DEFAULT NULL,
    depa_logr         INTEGER            NULL DEFAULT NULL,
    depa_logr_desc    VARCHAR(80)        NULL DEFAULT NULL,
    depa_ende         VARCHAR(160)       NULL DEFAULT NULL,
    depa_ende_nume    VARCHAR(20)        NULL DEFAULT NULL,
    depa_ende_comp    VARCHAR(80)        NULL DEFAULT NULL,
    depa_ende_bair    VARCHAR(80)        NULL DEFAULT NULL,
    depa_cida_codi    INTEGER            NULL DEFAULT NULL,
    depa_cida_desc    VARCHAR(100)       NULL DEFAULT NULL,
    depa_esta         VARCHAR(2)         NULL DEFAULT NULL,

    -- Contato
    depa_ddd1         VARCHAR(4)         NULL DEFAULT NULL,
    depa_fone1        VARCHAR(20)        NULL DEFAULT NULL,
    depa_emai         VARCHAR(120)       NULL DEFAULT NULL,

    -- Documento + Tomador (eSocial)
    depa_tipo_doc     INTEGER       NOT NULL DEFAULT 1,   -- 1=CNPJ / 2=CEI
    depa_cnpj         VARCHAR(14)        NULL DEFAULT NULL,
    depa_tipo_tomador INTEGER            NULL DEFAULT NULL,
    depa_tipo_tomador_desc VARCHAR(160)  NULL DEFAULT NULL,

    -- ===============================================================
    -- ABA 2: INFORMAÇÕES MENSAIS
    -- ===============================================================
    depa_im_terc      INTEGER            NULL DEFAULT NULL,
    depa_im_terc_desc VARCHAR(200)       NULL DEFAULT NULL,

    depa_fpas_codi    INTEGER            NULL DEFAULT NULL,
    depa_fpas_desc    VARCHAR(200)       NULL DEFAULT NULL,
    depa_fpas_perc    DECIMAL(10,2)      NULL DEFAULT NULL,

    depa_cnae_codi    INTEGER            NULL DEFAULT NULL,
    depa_cnae_desc    VARCHAR(250)       NULL DEFAULT NULL,
    depa_cnae_perc    DECIMAL(10,2)      NULL DEFAULT NULL,
    depa_fap_aliq     DECIMAL(14,4)      NULL DEFAULT NULL,

    depa_gps_pag_codi INTEGER            NULL DEFAULT NULL,
    depa_gps_pag_desc VARCHAR(220)       NULL DEFAULT NULL,
    depa_gps_transp_codi INTEGER         NULL DEFAULT NULL,
    depa_gps_transp_desc VARCHAR(220)    NULL DEFAULT NULL,

    -- Dados cadastrais / percentuais: 1=Nenhum, 2=Empresa, 3=Filial, 4=Departamento
    depa_dados_cad_codi  INTEGER    NOT NULL DEFAULT 1,
    depa_dados_perc_codi INTEGER    NOT NULL DEFAULT 1,
    depa_tx_servico      DECIMAL(14,2)   NULL DEFAULT NULL,
    depa_contab_codi     VARCHAR(40)    NULL DEFAULT NULL,
    depa_mensagens1      VARCHAR(255)   NULL DEFAULT NULL,
    depa_mensagens2      VARCHAR(255)   NULL DEFAULT NULL,

    -- ===============================================================
    -- LOGS
    -- ===============================================================
    depa_usuario_inc  VARCHAR(30)        NULL DEFAULT NULL,
    depa_data_inc     DATE          NULL DEFAULT NULL,
    depa_usuario_alt  VARCHAR(30)        NULL DEFAULT NULL,
    depa_data_alt     TIME          NULL DEFAULT NULL,

    -- PK REAL composta
    CONSTRAINT departamentosrh_pkey PRIMARY KEY (registro, depa_empr, depa_fili, depa_codi)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_departamentorh_desc
    ON public.departamentosrh (registro, depa_empr, depa_fili, depa_desc);

CREATE INDEX IF NOT EXISTS idx_departamentorh_inativo
    ON public.departamentosrh (registro, depa_empr, depa_fili, depa_inativo);

-- Permissões (ajuste o owner conforme seu ambiente)
ALTER TABLE public.departamentosrh OWNER TO postgres;
