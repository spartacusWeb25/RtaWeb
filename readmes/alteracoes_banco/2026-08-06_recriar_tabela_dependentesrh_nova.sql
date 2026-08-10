-- Estrutura NOVA da tabela public.dependentesrh
-- Padrao alinhado 100% com funcionarios: PK composta (registro+empresa+filial+funcionario+dependente)
-- Campos baseados NO SISTEMA LEGADO (print do usuario) - abas Cadastrais, Controle e Observacoes.
--
-- DATA: 2026-08-06
-- USO: Usuario vai APAGAR tabela antiga e rodar este script para a NOVA estrutura.
--
-- Ordem da CHAVE PRIMARIA (mesma ordem logica de navegacao do sistema legado):
--   1. registro    (licenca/CNPJ do cliente)
--   2. depe_empr   (empresa)
--   3. depe_fili   (filial)
--   4. depe_func   (funcionario dono do dependente)
--   5. depe_codi   (codigo sequencial do dependente por funcionario)

BEGIN;

DROP TABLE IF EXISTS public.dependentesrh CASCADE;

CREATE TABLE public.dependentesrh (
    -- ============================================================
    -- CHAVE PRIMARIA COMPOSTA (5 campos - igual a solicitacao)
    -- ============================================================
    registro varchar(14) NOT NULL,
    depe_empr integer NOT NULL,
    depe_fili integer NOT NULL,
    depe_func integer NOT NULL,
    depe_codi integer NOT NULL,

    -- ============================================================
    -- ABA: Cadastrais (campos do print legado)
    -- ============================================================
    -- Dados pessoais
    depe_nome varchar(120),
    depe_nascimento date,
    depe_cpf varchar(11),

    -- Dados certidao / registro civil
    depe_matricula varchar(30),
    depe_local_nascimento varchar(60),
    depe_cidade_codigo integer,
    depe_cidade varchar(60),
    depe_cartorio varchar(120),
    depe_numero_registro varchar(20),
    depe_numero_livro varchar(20),
    depe_numero_folha varchar(20),
    depe_data_entrega date,

    -- Tipo de dependencia / IRRF
    depe_tipo_dependencia integer,
    depe_data_baixa date,
    depe_ir_ate varchar(7),           -- Formato MM/AAAA (ex.: 08/2002) - "Dependente IR ate"
    depe_tipo_dependente integer,
    depe_tipo_dependente_desc varchar(60),
    depe_descricao_dependencia varchar(120),

    -- Flags
    depe_invalido boolean DEFAULT false,

    -- ============================================================
    -- ABA: Observacoes
    -- ============================================================
    depe_observacoes text,

    -- ============================================================
    -- CONSTRAINTS
    -- ============================================================
    CONSTRAINT dependentesrh_pkey
        PRIMARY KEY (registro, depe_empr, depe_fili, depe_func, depe_codi),

    CONSTRAINT dependentesrh_fkey_funcionario
        FOREIGN KEY (registro, depe_empr, depe_fili, depe_func)
        REFERENCES public.funcionarios (registro, func_empr, func_fili, func_codi)
        MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

-- ============================================================
-- COMMENTS (Documentacao da tabela e colunas)
-- ============================================================
COMMENT ON TABLE public.dependentesrh
    IS 'Cadastro de dependentes de funcionarios. Chave: registro + empresa + filial + codigo_funcionario + codigo_dependente.';

COMMENT ON COLUMN public.dependentesrh.registro
    IS 'Licenca/registro do cliente (CNPJ/CPF). Parte 1 da PK.';
COMMENT ON COLUMN public.dependentesrh.depe_empr
    IS 'Codigo da empresa (func_empr). Parte 2 da PK.';
COMMENT ON COLUMN public.dependentesrh.depe_fili
    IS 'Codigo da filial (func_fili). Parte 3 da PK.';
COMMENT ON COLUMN public.dependentesrh.depe_func
    IS 'Codigo do funcionario titular (func_codi). Parte 4 da PK.';
COMMENT ON COLUMN public.dependentesrh.depe_codi
    IS 'Codigo sequencial do dependente por funcionario. Parte 5 da PK.';

-- Dados pessoais
COMMENT ON COLUMN public.dependentesrh.depe_nome
    IS 'Nome completo do dependente.';
COMMENT ON COLUMN public.dependentesrh.depe_nascimento
    IS 'Data de nascimento.';
COMMENT ON COLUMN public.dependentesrh.depe_cpf
    IS 'CPF do dependente (11 digitos, sem pontuacao).';

-- Certidao / registro civil
COMMENT ON COLUMN public.dependentesrh.depe_matricula
    IS 'Matricula / numero da certidao (campo Matricula do sistema legado).';
COMMENT ON COLUMN public.dependentesrh.depe_local_nascimento
    IS 'Local de nascimento (municipio nasceu).';
COMMENT ON COLUMN public.dependentesrh.depe_cidade_codigo
    IS 'Codigo IBGE ou interno da cidade de nascimento.';
COMMENT ON COLUMN public.dependentesrh.depe_cidade
    IS 'Nome da cidade de nascimento (campo Cidade: descricao ao lado do codigo).';
COMMENT ON COLUMN public.dependentesrh.depe_cartorio
    IS 'Cartorio do registro civil.';
COMMENT ON COLUMN public.dependentesrh.depe_numero_registro
    IS 'Numero do registro de nascimento.';
COMMENT ON COLUMN public.dependentesrh.depe_numero_livro
    IS 'Numero do livro do cartorio.';
COMMENT ON COLUMN public.dependentesrh.depe_numero_folha
    IS 'Numero da folha / pagina do livro.';
COMMENT ON COLUMN public.dependentesrh.depe_data_entrega
    IS 'Data de entrega da documentacao na empresa.';

-- Tipo de dependencia
COMMENT ON COLUMN public.dependentesrh.depe_tipo_dependencia
    IS 'Tipo de dependencia: IR (Imposto de Renda), Previdencia, Plano saude, etc. (Combo do sistema legado).';
COMMENT ON COLUMN public.dependentesrh.depe_data_baixa
    IS 'Data em que deixou de ser dependente (baixa).';
COMMENT ON COLUMN public.dependentesrh.depe_ir_ate
    IS 'Formato MM/AAAA. Dependente IR ate (campo ao lado de Data da baixa no sistema legado).';
COMMENT ON COLUMN public.dependentesrh.depe_tipo_dependente
    IS 'Codigo do tipo de dependente (1=Filho, 2=Conjuge, etc.). Tabela de referencia do sistema legado.';
COMMENT ON COLUMN public.dependentesrh.depe_tipo_dependente_desc
    IS 'Descricao do tipo de dependente (campo a direita do codigo no sistema legado).';
COMMENT ON COLUMN public.dependentesrh.depe_descricao_dependencia
    IS 'Descricao livre da dependencia (campo cinza no sistema legado).';
COMMENT ON COLUMN public.dependentesrh.depe_invalido
    IS 'Checkbox Invalido (marcado = dependente nao valido / desconsiderar).';

-- Observacoes
COMMENT ON COLUMN public.dependentesrh.depe_observacoes
    IS 'Aba Observacoes. Texto livre / informacoes adicionais.';

COMMIT;
