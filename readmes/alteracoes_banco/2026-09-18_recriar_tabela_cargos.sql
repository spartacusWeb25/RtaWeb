-- 2026-09-18: Recriar tabela `cargos` com PK composta real 4 colunas
-- Obs: DELETE TABLE anterior antes para evitar conflito de colunas antigas (carg_cbo/carg_nome/carg_obse etc.)

DROP TABLE IF EXISTS public.cargos CASCADE;

CREATE TABLE public.cargos (
    registro character varying(14) NOT NULL,
    carg_empr integer NOT NULL,
    carg_fili integer NOT NULL,
    carg_codi integer NOT NULL,

    carg_descricao character varying(200),
    carg_inativo boolean DEFAULT false,
    carg_cbo_codi integer,
    carg_cbo_desc character varying(200),

    _log_data date,
    _log_time time without time zone,

    CONSTRAINT pk_cargos PRIMARY KEY (registro, carg_empr, carg_fili, carg_codi)
);

CREATE INDEX idx_cargos_codigo ON public.cargos (registro, carg_empr, carg_fili, carg_codi);
CREATE INDEX idx_cargos_descricao ON public.cargos (registro, upper((carg_descricao)::text));

ALTER TABLE public.cargos OWNER TO postgres;
