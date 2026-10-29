CREATE TABLE IF NOT EXISTS public.aumento_salarial (
    registro character varying(14) NOT NULL,
    aume_empr integer NOT NULL,
    aume_fili integer NOT NULL,
    aume_codi integer NOT NULL,
    aume_desc character varying(200) NULL,
    aume_func integer NULL,
    aume_data_alteracao date NULL,
    aume_data_efeito date NULL,
    aume_motivo character varying(200) NULL,
    aume_forma character varying(1) NULL,
    aume_valor numeric(15,2) NULL,
    aume_contribuintes boolean NULL DEFAULT FALSE,
    aume_tipo_funcionario character varying(1) NULL,
    aume_classe integer NULL,
    aume_cargo integer NULL,
    aume_departamento integer NULL,
    aume_centro_custo integer NULL,
    aume_sindicato integer NULL,
    aume_salario_atual numeric(15,2) NULL,
    aume_aumento_proporcional boolean NULL DEFAULT FALSE,
    aume_arredondar_salario boolean NULL DEFAULT FALSE,
    aume_alterar_meses_posteriores boolean NULL DEFAULT FALSE,
    aume_demitidos_mes boolean NULL DEFAULT FALSE,
    aume_admitidos_mes boolean NULL DEFAULT FALSE,
    aume_usuario_inc character varying(30) NULL,
    aume_data_inc date NULL,
    aume_usuario_alt character varying(30) NULL,
    aume_data_alt date NULL,
    _log_data date NULL,
    _log_time time without time zone NULL,
    CONSTRAINT aumento_salarial_pk PRIMARY KEY (
        registro,
        aume_empr,
        aume_fili,
        aume_codi
    )
);

CREATE INDEX IF NOT EXISTS aumento_salarial_lookup_idx
    ON public.aumento_salarial (registro, aume_empr, aume_fili, aume_func);

ALTER TABLE public.aumento_salarial
    ADD COLUMN IF NOT EXISTS aume_motivo character varying(200) NULL;
