-- =====================================================================
-- RECRIA TABELA terceiros 100% fiel ao models.py atualizado (18/09/2026)
-- ALTERACOES vs SQL antigo (2026-09-16):
--   1. CORRIGIDO: terc_cbo VARCHAR(10) -> INTEGER (agora combo codigo numerico)
--   2. INCLUIDO: terc_transportador_autonomo_perc_inss DECIMAL(5,2) (antes era ALTER TABLE separado, agora dentro da CREATE)
--   3. PK COMPOSTA REAL de 4 colunas: PRIMARY KEY (registro, terc_empr, terc_fili, terc_codi)
--      (igual unique_together do model; igual PK composta do dependentesterc)
--   4. MANTIDO NOME tabela = 'terceiros' (conforme solicitado pelo usuario; SEM prefixo cad_)
-- =====================================================================

DROP TABLE IF EXISTS public.terceiros CASCADE;

CREATE TABLE public.terceiros (
    -- PK COMPOSTA REAL (4 campos, igual unique_together do model e igual apps irmãos)
    registro                    varchar(14)     NOT NULL,
    terc_empr                   integer         NOT NULL,
    terc_fili                   integer         NOT NULL,
    terc_codi                   integer         NOT NULL,

    -- GERAL / HEADER
    terc_nome VARCHAR(200) NULL,
    terc_inativo BOOLEAN NULL,
    terc_data_admissao DATE NULL,

    -- ABA 1: CADASTRADOS
    terc_cpf VARCHAR(14) NULL,
    terc_cep VARCHAR(8) NULL,
    terc_logr INTEGER NULL,
    terc_ende VARCHAR(120) NULL,
    terc_ende_nume VARCHAR(20) NULL,
    terc_ende_comp VARCHAR(60) NULL,
    terc_ende_bair VARCHAR(60) NULL,
    terc_ende_cida_codi INTEGER NULL,
    terc_ende_cida_desc VARCHAR(60) NULL,
    terc_ende_uf VARCHAR(2) NULL,
    terc_ddd VARCHAR(4) NULL,
    terc_telefone VARCHAR(20) NULL,
    terc_ddd_celular VARCHAR(4) NULL,
    terc_celular VARCHAR(20) NULL,
    terc_email VARCHAR(200) NULL,

    -- ABA 2: DADOS GERAIS
    terc_nascimento DATE NULL,
    terc_cidade_nascimento_codi INTEGER NULL,
    terc_cidade_nascimento_desc VARCHAR(60) NULL,
    terc_naturalidade VARCHAR(2) NULL,
    terc_nome_mae VARCHAR(200) NULL,
    terc_grau_instrucao INTEGER NULL,
    terc_sexo INTEGER NULL,
    terc_estado_civil INTEGER NULL,
    terc_controlar_manual_dependentes_ir BOOLEAN NULL,
    terc_numero_dependentes_ir INTEGER NOT NULL DEFAULT 0,

    -- NACIONALIDADE / EXTERIOR (aba Cadastrais / Residencia exterior)
    terc_pais_nacionalidade_codi INTEGER NULL,
    terc_pais_nacionalidade_desc VARCHAR(80) NULL,
    terc_chegada_brasil DATE NULL,
    terc_casado_brasileiro BOOLEAN NULL,
    terc_tem_filhos_brasileiros BOOLEAN NULL,
    terc_rne VARCHAR(20) NULL,
    terc_orgao_uf_emissao_rne VARCHAR(30) NULL,
    terc_emissao_rne DATE NULL,
    terc_tempo_residencia INTEGER NULL,
    terc_condicao_ingresso INTEGER NULL,
    terc_pais_residencia_codi INTEGER NULL,
    terc_pais_residencia_desc VARCHAR(80) NULL,
    terc_residencia_exterior BOOLEAN NULL,
    terc_ende_exterior VARCHAR(120) NULL,
    terc_ende_exterior_nume VARCHAR(20) NULL,
    terc_ende_exterior_comp VARCHAR(60) NULL,
    terc_ende_exterior_bair VARCHAR(60) NULL,
    terc_ende_exterior_cidade VARCHAR(60) NULL,
    terc_ende_exterior_codigo_postal VARCHAR(20) NULL,

    -- ABA 3: DOCUMENTOS
    terc_banco INTEGER NULL,
    terc_banco_desc VARCHAR(120) NULL,
    terc_conta_corrente VARCHAR(20) NULL,
    terc_digito_conta_corrente VARCHAR(5) NULL,
    terc_tipo_conta INTEGER NULL,
    terc_modo_pagamento INTEGER NULL,
    terc_rg VARCHAR(20) NULL,
    terc_orgao_emissor_rg VARCHAR(20) NULL,
    terc_emissao_rg DATE NULL,
    terc_uf_rg VARCHAR(2) NULL,
    terc_certificado_reservista VARCHAR(30) NULL,
    terc_titulo_eleitor VARCHAR(20) NULL,
    terc_zona_titulo VARCHAR(5) NULL,
    terc_secao_titulo VARCHAR(5) NULL,
    terc_conselho_regional_numero VARCHAR(30) NULL,
    terc_conselho_regional_sigla VARCHAR(20) NULL,
    terc_ctps_numero VARCHAR(20) NULL,
    terc_ctps_serie VARCHAR(10) NULL,
    terc_ctps_digito VARCHAR(2) NULL,
    terc_ctps_data DATE NULL,
    terc_ctps_uf VARCHAR(2) NULL,
    terc_carne_inss_numero VARCHAR(20) NULL,
    terc_codigo_ccm VARCHAR(20) NULL,
    terc_carteira_identidade_arquivo BYTEA NULL,

    -- ABA 4: VINCULOS
    terc_classe INTEGER NULL,
    terc_classe_desc VARCHAR(120) NULL,
    terc_cbo INTEGER NULL,                         -- CORRIGIDO: agora INTEGER (nao VARCHAR(10))
    terc_cbo_desc VARCHAR(160) NULL,
    terc_natureza_ocupacao INTEGER NULL,
    terc_categoria_sefip INTEGER NULL,
    terc_categoria_esocial INTEGER NULL,
    terc_grau_risco INTEGER NULL,
    terc_transportador_autonomo_perc_inss DECIMAL(5,2) NOT NULL DEFAULT 0,  -- INCLUIDO no CREATE (antes era ALTER TABLE)
    terc_percentual_contr_ir DECIMAL(5,2) NOT NULL DEFAULT 0,
    terc_descontar_iss BOOLEAN NOT NULL DEFAULT FALSE,
    terc_percentual_iss DECIMAL(5,2) NOT NULL DEFAULT 0,
    terc_tributacao_irrf_exterior INTEGER NULL,
    terc_tributacao_irrf_exterior_desc VARCHAR(80) NULL,
    terc_rat_aposentadoria_perc DECIMAL(5,2) NOT NULL DEFAULT 0,
    terc_acordo_internacional_inss BOOLEAN NULL,
    terc_percentual_irrf_exterior DECIMAL(5,2) NOT NULL DEFAULT 0,
    terc_nif VARCHAR(30) NULL,
    terc_beneficiario_dispensado_nif BOOLEAN NULL,
    terc_pais_nao_exige_nif BOOLEAN NULL,
    terc_cartao_ponto INTEGER NULL,

    -- ABA 6: COMPLEMENTARES
    terc_tipo_sanguineo VARCHAR(5) NULL,
    terc_etnia_raca INTEGER NULL,
    terc_cor_cabelo INTEGER NULL,
    terc_cor_olhos INTEGER NULL,
    terc_pessoa_com_deficiencia BOOLEAN NULL,
    terc_observacoes_deficiencias TEXT NULL,
    terc_altura_metros DECIMAL(4,2) NULL,
    terc_peso_kg DECIMAL(5,2) NULL,
    terc_sinais_no_corpo BOOLEAN NULL,

    -- PK COMPOSTA REAL (4 colunas, igual unique_together no models.py)
    CONSTRAINT pk_terceiros
        PRIMARY KEY (registro, terc_empr, terc_fili, terc_codi)
);

-- Indices de performance: busca por nome/cpf/codigo empresa
CREATE INDEX terceiros_idx_nome
ON public.terceiros (terc_nome);

CREATE INDEX terceiros_idx_cpf
ON public.terceiros (terc_cpf);

CREATE INDEX terceiros_idx_empresa_filial
ON public.terceiros (registro, terc_empr, terc_fili);

-- Dono/tablespace: igual padrao PostgreSQL RTA
ALTER TABLE public.terceiros OWNER TO postgres;
