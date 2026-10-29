CREATE TABLE IF NOT EXISTS public.eventos_automaticos (
    registro character varying(14) NOT NULL,
    even_empr integer NOT NULL,
    even_fili integer NOT NULL,
    even_tipo_calculo character varying(2) NOT NULL,
    even_codi integer NOT NULL,
    _log_data date NULL,
    _log_time time without time zone NULL,
    CONSTRAINT eventos_automaticos_pk PRIMARY KEY (
        registro,
        even_empr,
        even_fili,
        even_tipo_calculo,
        even_codi
    )
);

CREATE INDEX IF NOT EXISTS eventos_automaticos_lookup_idx
    ON public.eventos_automaticos (registro, even_empr, even_fili, even_tipo_calculo);
