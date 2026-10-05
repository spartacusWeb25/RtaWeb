-- ============================================================================
-- DDL: Nova tabela public.prepara_rescisoes (Preparação de Rescisões)
-- PK COMPOSTA multi-tenant: registro + prep_empr + prep_fili + prep_codi
-- Script para rodar no PostgreSQL.
-- ============================================================================

DROP TABLE IF EXISTS public.prepara_rescisoes;

CREATE TABLE IF NOT EXISTS public.prepara_rescisoes (
    -- ===============================================================
    -- CHAVE PRIMÁRIA COMPOSTA 4 colunas (padrão projeto legado)
    -- ===============================================================
    registro          VARCHAR(14)   NOT NULL,
    prep_empr         INTEGER       NOT NULL DEFAULT 1,
    prep_fili         INTEGER       NOT NULL DEFAULT 1,
    prep_codi         INTEGER       NOT NULL,

    -- ===============================================================
    -- ABA 1: BÁSICOS (Código + Descrição)
    -- ===============================================================
    prep_desc         VARCHAR(200)  NOT NULL DEFAULT '',
    prep_descricao    VARCHAR(200)  NOT NULL DEFAULT '',

    -- ===============================================================
    -- ABA 2: DADOS GERAIS (superior tela SCI)
    -- ===============================================================
    -- Iniciativa: 1=Empresa, 2=Empregado, 3=Pedido Mútuo, etc.
    prep_iniciativa_codi      INTEGER            NULL DEFAULT NULL,

    -- Aviso prévio: 1=Aviso Indenizado, 2=Aviso Trabalhado, 3=Sem Aviso, 4=S/Data (S/Data = sem data certa)
    prep_aviso_previo_codi    INTEGER            NULL DEFAULT NULL,
    prep_inden_ferias_13      BOOLEAN            NULL DEFAULT FALSE,  -- Indenização 1/12 de férias e 13º

    -- Código saque FGTS (cod 23-00 = Rescisão Contratual por falecimento etc.)
    prep_saque_codi           VARCHAR(20)        NULL DEFAULT NULL,

    -- FGTS Código (ex: S2=Falecimento / etc)
    prep_fgts_codi            VARCHAR(20)        NULL DEFAULT NULL,

    -- FGTS Intermitente
    prep_fgts_int_codi        VARCHAR(20)        NULL DEFAULT NULL,

    -- CAGED / RAIS / GFD / HomologNet / eSocial
    prep_caged_codi           VARCHAR(20)        NULL DEFAULT NULL,
    prep_rais_codi            VARCHAR(20)        NULL DEFAULT NULL,
    prep_gfd_codi             VARCHAR(20)            NULL DEFAULT NULL,
    prep_homolognet_codi      VARCHAR(20)        NULL DEFAULT NULL,
    prep_motivo_esocial_codi  VARCHAR(20)        NULL DEFAULT NULL,

    -- ===============================================================
    -- ABA 3: CHECKBOXES INFERIORES (inferior tela SCI - blocos)
    -- ===============================================================
    prep_justa_causa          BOOLEAN       NOT NULL DEFAULT FALSE,
    prep_inden_contr_exp      BOOLEAN       NOT NULL DEFAULT FALSE,   -- Indenização contrato experiência
    prep_emitir_seg_desemp    BOOLEAN       NOT NULL DEFAULT FALSE,   -- Emitir seguro-desemprego
    prep_50_aviso_inden       BOOLEAN       NOT NULL DEFAULT FALSE,   -- 50% do aviso indenizado
    prep_estabilidade         BOOLEAN       NOT NULL DEFAULT FALSE,
    prep_nao_calc_multa_resc  BOOLEAN       NOT NULL DEFAULT FALSE,   -- Não calcula multa rescisória
    prep_50_verbas_inden      BOOLEAN       NOT NULL DEFAULT FALSE,   -- 50% das verbas indenizadas (aviso/férias/13º)

    -- Rescisão fixa (texto em vermelho na lateral direita do screenshot)
    prep_rescisao_fixa        BOOLEAN       NOT NULL DEFAULT FALSE,

    -- ===============================================================
    -- LOGS (padrão projeto: usuário + data inclusão / alteração)
    -- ===============================================================
    prep_usuario_inc          VARCHAR(30)        NULL DEFAULT NULL,
    prep_data_inc             DATE               NULL DEFAULT NULL,
    prep_usuario_alt          VARCHAR(30)        NULL DEFAULT NULL,
    prep_data_alt             DATE               NULL DEFAULT NULL,

    -- ===============================================================
    -- CHAVE PRIMÁRIA COMPOSTA (oficial)
    -- ===============================================================
    CONSTRAINT pk_prepara_rescisoes PRIMARY KEY (registro, prep_empr, prep_fili, prep_codi)
);

-- Índices de performance (pesquisa por empresa/filial e descrição)
CREATE INDEX IF NOT EXISTS ix_prepara_rescisoes_reg_empr_fili
    ON public.prepara_rescisoes (registro, prep_empr, prep_fili);

CREATE INDEX IF NOT EXISTS ix_prepara_rescisoes_desc
    ON public.prepara_rescisoes USING btree (prep_desc ASC NULLS LAST);

COMMENT ON TABLE  public.prepara_rescisoes                           IS 'Preparação de Rescisões - Tabela mestre com as opções/códigos usados nas rotinas de cálculo rescisório (CAGED, RAIS, FGTS, eSocial).';
COMMENT ON COLUMN public.prepara_rescisoes.registro                   IS 'CNPJ base da licença (multi-tenant) - sempre 14 dígitos, sem formatação.';
COMMENT ON COLUMN public.prepara_rescisoes.prep_empr                  IS 'Empresa (padrão 1).';
COMMENT ON COLUMN public.prepara_rescisoes.prep_fili                  IS 'Filial (padrão 1).';
COMMENT ON COLUMN public.prepara_rescisoes.prep_codi                  IS 'Código da preparação de rescisão (ex: 301 = Falecimento com mais de 1 ano).';
COMMENT ON COLUMN public.prepara_rescisoes.prep_desc                  IS 'Descrição curta do título da preparação de rescisão.';
COMMENT ON COLUMN public.prepara_rescisoes.prep_descricao             IS 'Descrição completa (na tela SCI: campo "Descrição" abaixo do Código).';
COMMENT ON COLUMN public.prepara_rescisoes.prep_iniciativa_codi       IS '1 = Empresa / 2 = Empregado / 3 = Pedido mútuo etc.';
COMMENT ON COLUMN public.prepara_rescisoes.prep_aviso_previo_codi     IS '1=Indenizado, 2=Trabalhado, 3=Sem Aviso, 4=S/Data.';
COMMENT ON COLUMN public.prepara_rescisoes.prep_50_verbas_inden       IS '50% das verbas indenizadas (aviso/férias/13º) - art. 477 §8º CLT.';
