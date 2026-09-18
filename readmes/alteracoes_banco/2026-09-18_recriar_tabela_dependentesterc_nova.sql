-- =================================================================
-- RECRIAÇÃO DA TABELA: public.dependentesterc (27 CAMPOS 1:1 TELA LEGADA)
-- Data: 18/09/2026
-- Motivo: Reescrever toda a estrutura de acordo com o models.py NOVO
--         (27 campos alinhados ao print legado "Cadastro de dependentes de terceiros")
--
-- OBSERVAÇÕES:
--  * PK REAL COMPOSTA de 5 colunas (padrão do projeto para dependentes):
--      (registro, depe_empr, depe_fili, depe_terc, depe_codi)
--  * managed=False no Django (nenhuma migration roda para esta tabela)
--  * Integridade referencial para terceiros é feita VIA CÓDIGO (views + delete custom)
--    e NÃO via FOREIGN KEY no banco, igual aos apps irmãos dependentesrh/dependentescontr.
-- =================================================================

DROP TABLE IF EXISTS public.dependentesterc CASCADE;

CREATE TABLE public.dependentesterc
(
    -- ===== PK COMPOSTA (5 colunas) =====
    registro                    varchar(14)     NOT NULL,
    depe_empr                   integer         NOT NULL,
    depe_fili                   integer         NOT NULL,
    depe_terc                   integer         NOT NULL,
    depe_codi                   integer         NOT NULL,

    -- ===== ABA CADASTRADOS (Campos 1:1 tela legada) =====
    depe_nome                   varchar(200),
    depe_nascimento             date,
    depe_matricula              varchar(30),
    depe_local_nascimento       varchar(60),
    depe_cidade_codigo          integer,
    depe_cidade                 varchar(60),
    depe_cartorio               varchar(120),
    depe_numero_registro        varchar(20),
    depe_numero_livro           varchar(20),
    depe_numero_folha           varchar(20),
    depe_data_entrega           date,
    depe_cpf                    varchar(14),
    depe_data_baixa             date,
    depe_ir_ate                 varchar(7),     -- Formato MM/AAAA (ex: 08/2002)
    depe_tipo_dependente        integer,
    depe_tipo_dependente_desc   varchar(60),
    depe_descricao_dependencia  varchar(255),
    depe_tipo_dependencia       integer,
    depe_invalido               boolean         DEFAULT false,

    -- ===== ABA OBSERVAÇÕES =====
    depe_observacoes            text,

    -- ===== RESTRIÇÕES =====
    CONSTRAINT pk_dependentesterc
        PRIMARY KEY (registro, depe_empr, depe_fili, depe_terc, depe_codi)
);

-- =================================================================
-- ÍNDICES PARA PERFORMANCE DE BUSCA (padrão apps irmãos)
-- =================================================================
CREATE INDEX idx_dependentesterc_terceiro_fk_logico
    ON public.dependentesterc (registro, depe_empr, depe_fili, depe_terc);

CREATE INDEX idx_dependentesterc_nome
    ON public.dependentesterc (registro, depe_nome);

CREATE INDEX idx_dependentesterc_cpf
    ON public.dependentesterc (registro, depe_cpf);

CREATE INDEX idx_dependentesterc_invalido
    ON public.dependentesterc (registro, depe_invalido);

-- =================================================================
-- OWNER (padrão do projeto)
-- =================================================================
ALTER TABLE  public.dependentesterc   OWNER TO postgres;
