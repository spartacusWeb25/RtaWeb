-- Reconstrução da tabela public.eventos DO ZERO
-- Estrutura 100% alinhada aos labels dos prints do sistema legado.
--
-- Convenção de nomes: todos os campos (exceto `registro`) usam prefixo `even_`
-- 3 abas:
--   1. Incidência
--   2. Características
--   3. Fórmulas
--
-- Chave primária composta REAL no PostgreSQL:  (registro, even_empr, even_codi)
--
-- ⚠️  ATENÇÃO
-- Este script APAGA TODOS OS DADOS da tabela public.eventos.
-- Tire um backup (pg_dump) antes de executar em ambientes com dados reais.
-- -----------------------------------------------------------------

BEGIN;

DROP TABLE IF EXISTS public.eventos;

CREATE TABLE public.eventos (

    -- ==================================================================
    -- 🔑 CHAVE COMPOSTA (nomes preservados conforme solicitado)
    -- ==================================================================
    registro                        varchar(14)   NOT NULL,
    even_empr                       integer       NOT NULL,
    even_codi                       integer       NOT NULL,

    -- ==================================================================
    -- 🧾 CABEÇALHO (sempre visível, acima das abas)
    -- ==================================================================
    even_desc                  varchar(120),
    even_inativo                    boolean,

    -- ==================================================================
    -- 📊 ABA 1 — INCIDÊNCIA
    -- ==================================================================
    -- Classificação / Natureza da rubrica
    even_classificacao              varchar(30),
    even_natureza_rubrica           varchar(6),

    -- Tipos / Referência
    even_tipo_referencia            integer,    -- Dinheiro / Percentual / Quantidade / Dia / Hora ...
    even_tipo_verba                 integer,       -- Provento / Desconto / Base / Informativa

    -- Incidências tributárias (combobox 0..3 — "Não Incide", "Incide Normalmente", etc.)
    even_incide_inss                boolean,
    even_incide_fgts                boolean,
    even_incide_ir                  boolean,
    even_incide_pis_pasep           boolean,
    even_incide_contribuicoes_sindicais boolean,
    even_incide_base_salario_familia boolean,

    -- Códigos eSocial (4 colunas independentes, como no legado)
    even_esocial_1                  varchar(6),
    even_esocial_2                  varchar(6),
    even_esocial_3                  varchar(6),
    even_esocial_4                  varchar(6),

    -- ==================================================================
    -- ⚙️ ABA 2 — CARACTERÍSTICAS
    -- ==================================================================
    -- Horas extras (checkbox + percentual + símbolo %)
    even_flag_horas_extras          boolean,
    even_percentual_horas_extras    numeric(10,4),

    -- Flags em grid 3 colunas (exatamente como exibido no legado)
    even_rendimento_variavel            boolean,
    even_comissao                       boolean,
    even_dsr_salario                    boolean,
    even_dsr_horas_extras               boolean,
    even_dsr_rendimentos_variaveis      boolean,
    even_indenizacao_rescisao_contrato  boolean,
    even_ajuda_custo_diarias            boolean,
    even_grava_ficha_horas_normais      boolean,
    even_adicional_dirigente_sindical   boolean,
    even_media_horas_adicional_noturno  boolean,
    even_plano_saude_empresarial        boolean,
    even_reembolso_despesas_medicas     boolean,
    even_despesas_judiciarias           boolean,
    even_distribuicao_lucros            boolean,
    even_previdencia_privada            boolean,
    even_fapi                           boolean,
    even_pensao_alimenticia             boolean,
    even_previdencia_oficial            boolean,
    even_desconto_compulsorio           boolean,
    even_salario_garantia               boolean,
    even_taxa_servico                   boolean,
    even_medias_sobre_valores           boolean,
    even_somente_tomador_principal      boolean,
    even_rendimento_isento_irrf         boolean,
    even_nao_considera_para_estouro     boolean,
    even_descontar_pensao_paga_13       boolean,
    even_descontar_pensao_paga_adto13   boolean,
    even_imprimir_verba_zerada          boolean,
    even_ferias_folha_credito_trabalha  boolean,

    -- Órgão público
    even_teto_remuneratorio_cf      integer,   -- Teto art. 37 XI CF/88
    even_incidencia_cprp            integer,
    even_funcionarios_afastados     integer,

    even_verba_negativa_esocial         varchar(6),

    -- Observação
    even_observacao                 text,

    -- ==================================================================
    -- 🧮 ABA 3 — FÓRMULAS
    -- ==================================================================
    even_formula_ref1               varchar(200),
    even_formula_ref2               varchar(200),
    even_formula_ref3               varchar(200),
    even_formula_valo1              varchar(200),
    even_formula_valo2              varchar(200),
    even_formula_valo3              varchar(200),

    -- ==================================================================
    -- 🗂️ Controle de auditoria (colunas físicas do legado)
    -- ==================================================================
    _log_data                       date,
    _log_time                       time,

    -- ==================================================================
    -- Restrições e índices
    -- ==================================================================
    CONSTRAINT pk_eventos PRIMARY KEY (registro, even_empr, even_codi)
);

-- Índices secundários para acelerar filtros frequentes
CREATE INDEX idx_eventos_descricao         ON public.eventos USING btree (even_desc);
CREATE INDEX idx_eventos_natureza_rubrica  ON public.eventos USING btree (even_natureza_rubrica);
CREATE INDEX idx_eventos_tipo_verba        ON public.eventos USING btree (even_tipo_verba);

COMMIT;
