CREATE TABLE IF NOT EXISTS public.eventos_agrupados (
    registro character varying(14) NOT NULL,
    even_empr integer NOT NULL,
    even_fili integer NOT NULL,
    even_ferias_proporcionais integer NULL,
    even_ferias_vencidas integer NULL,
    even_ferias_dobro integer NULL,
    even_ferias_indenizadas integer NULL,
    even_13_salario integer NULL,
    even_13_salario_indenizado integer NULL,
    even_aviso_previo_indenizado integer NULL,
    CONSTRAINT eventos_agrupados_pk PRIMARY KEY (registro, even_empr, even_fili)
);

CREATE INDEX IF NOT EXISTS eventos_agrupados_idx1
    ON public.eventos_agrupados (registro, even_empr, even_fili);
