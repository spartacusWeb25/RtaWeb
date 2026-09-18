-- ============================================================================
-- 2026-09-18 Recriar tabela `horarios` (Plano de quadros de horários)
-- Padrão PK COMPOSTA REAL: registro + hora_empr + hora_fili + hora_codi
-- ============================================================================

-- 1) Remover tabela antiga se existir (DROP CASCADE para índices/constraints)
DROP TABLE IF EXISTS public.horarios CASCADE;

-- 2) Criar tabela NOVA
CREATE TABLE public.horarios (
    -- ===== PK COMPOSTA REAL (4 colunas) =====
    registro            VARCHAR(14) NOT NULL,
    hora_empr           INTEGER     NOT NULL,
    hora_fili           INTEGER     NOT NULL,
    hora_codi           INTEGER     NOT NULL,

    -- ===== CAMPOS CABEÇALHO (1 registro = 1 quadro) =====
    hora_nome           VARCHAR(250),
    hora_flexivel       BOOLEAN     DEFAULT FALSE,
    hora_total_semana   VARCHAR(10),
    hora_folga_alt      BOOLEAN     DEFAULT FALSE,

    -- Checkboxes de folga por dia
    hora_folga_dom      BOOLEAN     DEFAULT FALSE,
    hora_folga_seg      BOOLEAN     DEFAULT FALSE,
    hora_folga_ter      BOOLEAN     DEFAULT FALSE,
    hora_folga_qua      BOOLEAN     DEFAULT FALSE,
    hora_folga_qui      BOOLEAN     DEFAULT FALSE,
    hora_folga_sex      BOOLEAN     DEFAULT FALSE,
    hora_folga_sab      BOOLEAN     DEFAULT FALSE,

    hora_desc_esocial   TEXT,

    -- ===== CAMPOS POR DIA DA SEMANA (7 dias × 11 campos = 77 cols) =====
    -- ===== DOMINGO =====
    hora_dom_esoc       INTEGER,
    hora_dom_inic_1     VARCHAR(8),
    hora_dom_fina_1     VARCHAR(8),
    hora_dom_lanc_inic_1 VARCHAR(8),
    hora_dom_lanc_fina_1 VARCHAR(8),
    hora_dom_inic_2     VARCHAR(8),
    hora_dom_fina_2     VARCHAR(8),
    hora_dom_lanc_inic_2 VARCHAR(8),
    hora_dom_lanc_fina_2 VARCHAR(8),
    hora_dom_intervalo  VARCHAR(10),
    hora_dom_jornada    VARCHAR(10),

    -- ===== SEGUNDA-FEIRA =====
    hora_seg_esoc       INTEGER,
    hora_seg_inic_1     VARCHAR(8),
    hora_seg_fina_1     VARCHAR(8),
    hora_seg_lanc_inic_1 VARCHAR(8),
    hora_seg_lanc_fina_1 VARCHAR(8),
    hora_seg_inic_2     VARCHAR(8),
    hora_seg_fina_2     VARCHAR(8),
    hora_seg_lanc_inic_2 VARCHAR(8),
    hora_seg_lanc_fina_2 VARCHAR(8),
    hora_seg_intervalo  VARCHAR(10),
    hora_seg_jornada    VARCHAR(10),

    -- ===== TERÇA-FEIRA =====
    hora_ter_esoc       INTEGER,
    hora_ter_inic_1     VARCHAR(8),
    hora_ter_fina_1     VARCHAR(8),
    hora_ter_lanc_inic_1 VARCHAR(8),
    hora_ter_lanc_fina_1 VARCHAR(8),
    hora_ter_inic_2     VARCHAR(8),
    hora_ter_fina_2     VARCHAR(8),
    hora_ter_lanc_inic_2 VARCHAR(8),
    hora_ter_lanc_fina_2 VARCHAR(8),
    hora_ter_intervalo  VARCHAR(10),
    hora_ter_jornada    VARCHAR(10),

    -- ===== QUARTA-FEIRA =====
    hora_qua_esoc       INTEGER,
    hora_qua_inic_1     VARCHAR(8),
    hora_qua_fina_1     VARCHAR(8),
    hora_qua_lanc_inic_1 VARCHAR(8),
    hora_qua_lanc_fina_1 VARCHAR(8),
    hora_qua_inic_2     VARCHAR(8),
    hora_qua_fina_2     VARCHAR(8),
    hora_qua_lanc_inic_2 VARCHAR(8),
    hora_qua_lanc_fina_2 VARCHAR(8),
    hora_qua_intervalo  VARCHAR(10),
    hora_qua_jornada    VARCHAR(10),

    -- ===== QUINTA-FEIRA =====
    hora_qui_esoc       INTEGER,
    hora_qui_inic_1     VARCHAR(8),
    hora_qui_fina_1     VARCHAR(8),
    hora_qui_lanc_inic_1 VARCHAR(8),
    hora_qui_lanc_fina_1 VARCHAR(8),
    hora_qui_inic_2     VARCHAR(8),
    hora_qui_fina_2     VARCHAR(8),
    hora_qui_lanc_inic_2 VARCHAR(8),
    hora_qui_lanc_fina_2 VARCHAR(8),
    hora_qui_intervalo  VARCHAR(10),
    hora_qui_jornada    VARCHAR(10),

    -- ===== SEXTA-FEIRA =====
    hora_sex_esoc       INTEGER,
    hora_sex_inic_1     VARCHAR(8),
    hora_sex_fina_1     VARCHAR(8),
    hora_sex_lanc_inic_1 VARCHAR(8),
    hora_sex_lanc_fina_1 VARCHAR(8),
    hora_sex_inic_2     VARCHAR(8),
    hora_sex_fina_2     VARCHAR(8),
    hora_sex_lanc_inic_2 VARCHAR(8),
    hora_sex_lanc_fina_2 VARCHAR(8),
    hora_sex_intervalo  VARCHAR(10),
    hora_sex_jornada    VARCHAR(10),

    -- ===== SÁBADO =====
    hora_sab_esoc       INTEGER,
    hora_sab_inic_1     VARCHAR(8),
    hora_sab_fina_1     VARCHAR(8),
    hora_sab_lanc_inic_1 VARCHAR(8),
    hora_sab_lanc_fina_1 VARCHAR(8),
    hora_sab_inic_2     VARCHAR(8),
    hora_sab_fina_2     VARCHAR(8),
    hora_sab_lanc_inic_2 VARCHAR(8),
    hora_sab_lanc_fina_2 VARCHAR(8),
    hora_sab_intervalo  VARCHAR(10),
    hora_sab_jornada    VARCHAR(10),

    -- ===== LOGS =====
    _log_data           DATE,
    _log_time           TIME,

    -- ===== CONSTRAINT PK COMPOSTA REAL =====
    CONSTRAINT horarios_pkey PRIMARY KEY (registro, hora_empr, hora_fili, hora_codi)
);

-- ===== OWNER =====
ALTER TABLE public.horarios OWNER TO postgres;

-- ===== ÍNDICES =====
CREATE INDEX idx_horarios_codi
    ON public.horarios (registro, hora_codi);

CREATE INDEX idx_horarios_nome
    ON public.horarios (registro, upper((hora_nome)::text));

CREATE INDEX idx_horarios_empr_fili
    ON public.horarios (registro, hora_empr, hora_fili);

-- ============================================================================
-- Fim do script
-- ============================================================================
