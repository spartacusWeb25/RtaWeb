BEGIN;

DROP TABLE IF EXISTS dependentescontr;

CREATE TABLE dependentescontr (
    registro VARCHAR(14) NOT NULL,
    depecontr_empr INTEGER NOT NULL,
    depecontr_fili INTEGER NOT NULL,
    depecontr_contr INTEGER NOT NULL,
    depecontr_codi INTEGER NOT NULL,
    depecontr_nome VARCHAR(200),
    depecontr_nascimento DATE,
    depecontr_cpf VARCHAR(14),
    depecontr_matricula VARCHAR(30),
    depecontr_local_nascimento VARCHAR(60),
    depecontr_cidade_codigo INTEGER,
    depecontr_cidade VARCHAR(60),
    depecontr_cartorio VARCHAR(120),
    depecontr_numero_registro VARCHAR(20),
    depecontr_numero_livro VARCHAR(20),
    depecontr_numero_folha VARCHAR(20),
    depecontr_data_entrega DATE,
    depecontr_tipo_dependencia INTEGER,
    depecontr_data_baixa DATE,
    depecontr_ir_ate VARCHAR(7),
    depecontr_tipo_dependente INTEGER,
    depecontr_invalido BOOLEAN DEFAULT FALSE,
    depecontr_observacoes TEXT,
    depecontr_grau_parentesco INTEGER,
    depecontr_pensao_alimenticia_valor DECIMAL(15,2),
    depecontr_pensao_alimenticia_percentual DECIMAL(8,4),
    depecontr_dependente_irrf BOOLEAN DEFAULT FALSE,
    depecontr_dependente_salario_familia BOOLEAN DEFAULT FALSE,
    depecontr_rg VARCHAR(20),
    depecontr_orgao_emissor_rg VARCHAR(20),
    depecontr_uf_rg VARCHAR(2),
    depecontr_emissao_rg DATE,
    depecontr_certidao_nascimento VARCHAR(30),
    depecontr_desc_dependencia VARCHAR(255),
    PRIMARY KEY (registro, depecontr_empr, depecontr_fili, depecontr_contr, depecontr_codi)
);

CREATE INDEX idx_dependentescontr_nome ON dependentescontr (registro, depecontr_nome);
CREATE INDEX idx_dependentescontr_cpf ON dependentescontr (registro, depecontr_cpf);
CREATE INDEX idx_dependentescontr_contr ON dependentescontr (registro, depecontr_empr, depecontr_fili, depecontr_contr);
CREATE INDEX idx_dependentescontr_tipo_dependente ON dependentescontr (registro, depecontr_tipo_dependente);
CREATE INDEX idx_dependentescontr_tipo_dependencia ON dependentescontr (registro, depecontr_tipo_dependencia);

COMMIT;
