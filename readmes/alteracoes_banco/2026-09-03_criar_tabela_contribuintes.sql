-- Criacao da tabela public.contribuintes DO ZERO
-- Estrutura 100% alinhada aos labels dos prints do sistema legado.
--
-- Convenção de nomes: todos os campos (exceto `registro`) usam prefixo `contr_`
-- 13 abas:
--   1. Cadastrais
--   2. Físico
--   3. Histórico
--   4. Estrangeiro
--   5. Documentos
--   6. Dependentes
--   7. FGTS/GPS
--   8. Vínculos
--   9. Cálculo
--  10. Banco
--  11. eSocial (2 sub-abas: Qualificação + Integração)
--  12. Observações gerais
--
-- Chave primária composta REAL no PostgreSQL:  (registro, contr_empr, contr_fili, contr_codi)
--
-- ⚠️  ATENÇÃO
-- Este script APAGA TODOS OS DADOS da tabela public.contribuintes.
-- Tire um backup (pg_dump) antes de executar em ambientes com dados reais.
-- -----------------------------------------------------------------

BEGIN;

DROP TABLE IF EXISTS public.contribuintes;

CREATE TABLE public.contribuintes (

    -- ==================================================================
    --  CHAVE COMPOSTA (nomes preservados conforme solicitado)
    -- ==================================================================
    registro                            varchar(14)   NOT NULL,
    contr_empr                          integer       NOT NULL,
    contr_fili                          integer       NOT NULL,
    contr_codi                          integer       NOT NULL,

    -- ==================================================================
    --  ABA 1 — CADASTRIS
    -- ==================================================================
    contr_admissao_preliminar           integer,
    contr_nome                          varchar(200)  NOT NULL,
    contr_email                         varchar(200),
    contr_matricula_esocial             varchar(30),

    -- Endereço
    contr_cep                           varchar(8),
    contr_logr                          integer,
    contr_ende                          varchar(120),
    contr_ende_nume                     varchar(20),
    contr_ende_comp                     varchar(60),
    contr_ende_bair                     varchar(60),
    contr_ende_cida_codi                integer,
    contr_ende_cida_desc                varchar(60),
    contr_ende_uf                       varchar(2),
    contr_ddd                           varchar(4),
    contr_telefone                      varchar(20),
    contr_ddd_celular                   varchar(4),
    contr_celular                       varchar(20),

    -- Residência no exterior
    contr_residencia_exterior           boolean,
    contr_pais_residencia_codi          integer,
    contr_pais_residencia_desc          varchar(80),
    contr_ende_exterior                 varchar(120),
    contr_ende_exterior_nume            varchar(20),
    contr_ende_exterior_comp            varchar(60),
    contr_ende_exterior_bair            varchar(60),
    contr_ende_exterior_cidade          varchar(60),
    contr_ende_exterior_codigo_postal   varchar(20),

    -- ==================================================================
    --  ABA 2 — FÍSICO
    -- ==================================================================
    contr_tipo_sanguineo                varchar(5),
    contr_etnia_raca                    integer,
    contr_sexo                          integer,
    contr_deficiencia                   boolean,
    contr_deficiencia_fisica            boolean,
    contr_deficiencia_auditiva          boolean,
    contr_deficiencia_visual            boolean,
    contr_deficiencia_intelectual       boolean,
    contr_deficiencia_mental            boolean,
    contr_reabilitado                   boolean,
    contr_foto_3x4                      bytea,
    contr_observacoes_deficiencias      text,

    -- ==================================================================
    -- ABA 3 — HISTÓRICO
    -- ==================================================================
    contr_pais_nascimento_codi          integer,
    contr_pais_nascimento_desc          varchar(80),
    contr_cidade_nascimento_codi        integer,
    contr_cidade_nascimento_desc        varchar(60),
    contr_naturalidade                  varchar(2),
    contr_nascimento                    date,
    contr_estado_civil                  integer,
    contr_grau_instrucao                integer,
    contr_data_entrada                  date,
    contr_data_cadastro                 date,
    contr_inicio_adicional_tempo_servico date,
    contr_data_baixa                    date,
    contr_data_pagamento_baixa          date,
    contr_motivo_desligamento           integer,
    contr_esocial_indicativo_pensao_alimenticia_fgts integer,
    contr_pensao_fgts_valor             numeric(15,2),
    contr_pensao_fgts_percentual        numeric(5,2),

    -- ==================================================================
    --  ABA 4 — ESTRANGEIRO
    -- ==================================================================
    contr_pais_nacionalidade_codi       integer,
    contr_pais_nacionalidade_desc       varchar(80),
    contr_chegada_brasil                date,
    contr_casado_brasileiro             boolean,
    contr_tem_filhos_brasileiros        boolean,
    contr_rne                           varchar(20),
    contr_orgao_uf_emissao_rne          varchar(30),
    contr_emissao_rne                   date,
    contr_tempo_residencia              integer,
    contr_condicao_ingresso             integer,

    -- ==================================================================
    --  ABA 5 — DOCUMENTOS
    -- ==================================================================
    contr_cpf                           varchar(14),
    contr_nis                           varchar(14),
    contr_emissao_nis                   date,          -- data emissao PIS/NIS
    contr_rg                            varchar(20),
    contr_orgao_emissor_rg              varchar(20),
    contr_uf_rg                         varchar(2),
    contr_emissao_rg                    date,
    contr_carteira_trabalho             varchar(20),
    contr_serie_carteira_trabalho       varchar(10),
    contr_digito_serie_carteira_trabalho varchar(2),
    contr_uf_carteira_trabalho          varchar(2),
    contr_emissao_carteira_trabalho     date,
    contr_cnh                           varchar(20),
    contr_categoria_cnh                 varchar(5),
    contr_uf_cnh                        varchar(2),
    contr_emissao_cnh                   date,
    contr_vencimento_cnh                date,
    contr_primeira_habilitacao          date,
    contr_titulo_eleitor                varchar(20),
    contr_zona_titulo_eleitor           varchar(5),
    contr_secao_titulo_eleitor          varchar(5),
    contr_certificado_reservista        varchar(30),
    contr_carteira_identidade_arquivo   bytea,
    contr_aviso_carteira_trabalho_digital boolean DEFAULT true,

    -- ==================================================================
    --  ABA 6 — DEPENDENTES (campos no próprio contribuinte)
    -- ==================================================================
    contr_nome_pai                      varchar(200)  NULL,
    contr_nome_mae                      varchar(200)  NULL,
    contr_tem_dependentes               boolean       NULL DEFAULT false,

    -- ==================================================================
    --  ABA 7 — FGTS/GPS
    -- ==================================================================
    contr_categoria_sefip               integer       NULL,
    contr_categoria_esocial             integer       NULL,
    contr_categoria_esocial_desc        varchar(120)  NULL,
    contr_transp_autonomo_contribuicao_inss numeric(5,2) NULL,
    contr_percentual_contr_ir           numeric(5,2)  NULL,
    contr_data_opcao                    date          NULL,
    contr_percentual_fgts               numeric(5,2)  NULL,
    contr_grau_risco                    integer       NULL,
    contr_rat_aposentadoria             numeric(5,2)  NULL,
    contr_descontar_iss                 boolean       NULL,
    contr_percentual_iss                numeric(5,2)  NULL,
    contr_regime_previdenciario         integer       NULL,
    contr_categoria_origem              integer       NULL,
    contr_tipo_cnpj_cpf_origem          integer       NULL,
    contr_cnpj_cpf_origem               varchar(14)   NULL,
    contr_admissao_origem               date          NULL,
    contr_matricula_origem              varchar(30)   NULL,
    contr_regime_previdenciario_origem  integer       NULL,

    -- ==================================================================
    --  ABA 8 — VÍNCULOS
    -- ==================================================================
    contr_classe                        integer       NULL,
    contr_vinculo_empregaticio          integer       NULL,
    contr_vinculo_empregaticio_desc     varchar(120)  NULL,
    contr_depto                         integer       NULL,
    contr_depto_desc                    varchar(120)  NULL,
    contr_ccusto                        integer       NULL,
    contr_ccusto_desc                   varchar(120)  NULL,
    contr_cargo                         integer       NULL,
    contr_cargo_desc                    varchar(120)  NULL,
    contr_cbo                           varchar(10)   NULL,
    contr_cbo_desc                      varchar(120)  NULL,
    contr_natureza_ocupacao             integer       NULL,
    contr_orgao_classe                  boolean       NULL,
    contr_inscricao_orgao_classe        varchar(30)   NULL,
    contr_orgao_uf_emissao_orgao_classe varchar(30)   NULL,
    contr_emissao_orgao_classe          date          NULL,
    contr_validade_orgao_classe         date          NULL,

    -- ==================================================================
    --  ABA 9 — CÁLCULO
    -- ==================================================================
    contr_forma_pagamento               integer       NULL,
    contr_remuneracao                   numeric(15,2) NULL,
    contr_nao_arredondar                boolean       NULL,
    contr_descontar_inss_do_ir          boolean       NULL,
    contr_adiantamento                  boolean       NULL,
    contr_valor_previdencia_privada     numeric(15,2) NULL,
    contr_valor_previdencia_privada_13  numeric(15,2) NULL,
    contr_aplica_deducao_mais_benefica_irrf boolean    NULL,
    contr_base_inss_multiplos_vinculos  numeric(15,2) NULL,
    contr_valor_inss_multiplos_vinculos numeric(15,2) NULL,
    contr_base_ir_multiplos_vinculos    numeric(15,2) NULL,
    contr_valor_ir_multiplos_vinculos   numeric(15,2) NULL,
    contr_base_inss_multiplos_vinculos_13 numeric(15,2) NULL,
    contr_valor_inss_multiplos_vinculos_13 numeric(15,2) NULL,
    contr_base_ir_multiplos_vinculos_13 numeric(15,2) NULL,
    contr_valor_ir_multiplos_vinculos_13 numeric(15,2) NULL,

    -- ==================================================================
    -- ABA 10 — BANCO
    -- ==================================================================
    contr_banco                         integer       NULL,
    contr_banco_desc                    varchar(120)  NULL,
    contr_conta_corrente                varchar(20)   NULL,
    contr_digito_conta_corrente         varchar(5)    NULL,
    contr_tipo_conta                    integer       NULL,
    contr_modo_pagamento                integer       NULL,

    -- ==================================================================
    --  ABA 12 eSocial: sub-abas Qualificação + Integração
    -- ==================================================================
    contr_esocial_qualif_status          varchar(500)  NULL,
    contr_esocial_qualif_mensagem        text          NULL,
    contr_esocial_qualif_data_hora       timestamp     NULL,
    contr_esocial_integrado              boolean       NULL DEFAULT false,
    contr_esocial_integra_data_hora      timestamp     NULL,
    contr_esocial_integra_numero_recibo  varchar(80)   NULL,

    -- ==================================================================
    --  ABA 13 Observações gerais: contr_observacoes (TEXT, JA EXISTE acima)
    -- ==================================================================

    -- ==================================================================
    -- Restrições e índices
    -- ==================================================================
    CONSTRAINT pk_contribuintes PRIMARY KEY (registro, contr_empr, contr_fili, contr_codi)
);

-- Índices secundários para acelerar filtros frequentes
CREATE INDEX idx_contribuintes_nome               ON public.contribuintes USING btree (contr_nome);
CREATE INDEX idx_contribuintes_cpf                ON public.contribuintes USING btree (contr_cpf);
CREATE INDEX idx_contribuintes_matricula_esocial  ON public.contribuintes USING btree (contr_matricula_esocial);

COMMIT;
