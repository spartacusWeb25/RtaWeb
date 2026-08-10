-- Table: public.classes_funcionario

-- DROP TABLE IF EXISTS public.classes_funcionario;

CREATE TABLE IF NOT EXISTS public.classes_funcionario
(
    clas_codi integer NOT NULL,
    clas_desc character varying(60) COLLATE pg_catalog."default" NOT NULL,
    clas_grupo character varying(30) COLLATE pg_catalog."default",
    clas_reducao_base_ir boolean DEFAULT false,
    CONSTRAINT classes_funcionario_pkey PRIMARY KEY (clas_codi)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.classes_funcionario
    OWNER to postgres;

COMMENT ON TABLE public.classes_funcionario
    IS 'Tabela de apoio para classes de funcionarios.';

COMMENT ON COLUMN public.classes_funcionario.clas_codi
    IS 'Codigo da classe.';

COMMENT ON COLUMN public.classes_funcionario.clas_desc
    IS 'Descricao da classe.';

COMMENT ON COLUMN public.classes_funcionario.clas_grupo
    IS 'Grupo da classe.';

COMMENT ON COLUMN public.classes_funcionario.clas_reducao_base_ir
    IS 'Indica se ha reducao na base do IR.';

