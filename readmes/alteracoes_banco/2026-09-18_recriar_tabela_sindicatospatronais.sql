-- ============================================================
-- RECRIAR TABELA sindicatospatronais (Sindicatos Patronais)
-- PK COMPOSTA REAL de 4 colunas
-- Data: 2026-09-18
-- ============================================================

BEGIN;

DROP TABLE IF EXISTS sindicatospatronais CASCADE;

CREATE TABLE sindicatospatronais (
    registro varchar(14) NOT NULL,
    sind_empr integer NOT NULL,
    sind_fili integer NOT NULL,
    sind_codi integer NOT NULL,

    sind_nome varchar(200),
    sind_tipo_entidade integer,
    sind_entidade varchar(20),
    sind_codi_sind varchar(15),
    sind_agencia_grcs integer,
    sind_codi_cede varchar(15),
    sind_cep varchar(8),
    sind_logr integer,
    sind_ende varchar(120),
    sind_ende_nume varchar(20),
    sind_ende_comp varchar(60),
    sind_ende_bair varchar(60),
    sind_cida_codi integer,
    sind_cida_desc varchar(60),
    sind_esta varchar(2),
    sind_ddd1 varchar(4),
    sind_fone1 varchar(20),
    sind_ddd2 varchar(4),
    sind_fone2 varchar(20),
    sind_cnpj varchar(14),
    sind_tabela integer,
    sind_site varchar(150),
    sind_emai varchar(100),
    _log_data date,
    _log_time time,

    CONSTRAINT pk_sindicatospatronais PRIMARY KEY (registro, sind_empr, sind_fili, sind_codi)
);

CREATE INDEX idx_sindpat_nome ON sindicatospatronais (sind_nome);
CREATE INDEX idx_sindpat_cnpj ON sindicatospatronais (sind_cnpj);
CREATE INDEX idx_sindpat_codigo ON sindicatospatronais (registro, sind_empr, sind_fili, sind_codi);

ALTER TABLE sindicatospatronais OWNER TO postgres;

COMMIT;
