-- Script de alteracao de banco referente aos ajustes do dia 2026-06-22
-- Objetivo:
-- 1. Adicionar o campo tabe_mini_gps em tabelainss
-- 2. Adicionar os campos irrf_desc_mini e irrf_desc_simp em tabelairrf
--
-- Observacoes:
-- - Script pensado para PostgreSQL.
-- - As alteracoes sao nao destrutivas: apenas adicionam colunas novas.
-- - As colunas antigas NAO sao removidas por este script.
-- - Se houver necessidade de carga inicial de dados, faça isso em um passo separado.

BEGIN;

ALTER TABLE public.tabelainss
    ADD COLUMN IF NOT EXISTS tabe_mini_gps NUMERIC(15,2);

ALTER TABLE public.tabelairrf
    ADD COLUMN IF NOT EXISTS irrf_desc_mini NUMERIC(15,2);

ALTER TABLE public.tabelairrf
    ADD COLUMN IF NOT EXISTS irrf_desc_simp NUMERIC(15,2);

COMMIT;

-- Validacao rapida apos executar:
-- SELECT column_name, data_type, numeric_precision, numeric_scale
-- FROM information_schema.columns
-- WHERE table_schema = 'public'
--   AND table_name IN ('tabelainss', 'tabelairrf')
--   AND column_name IN ('tabe_mini_gps', 'irrf_desc_mini', 'irrf_desc_simp')
-- ORDER BY table_name, column_name;

-- Caso deseje popular os novos campos com algum valor inicial,
-- execute um UPDATE separado depois de validar a regra de negocio.
