-- Estrutura base da tabela public.funcionarios
-- RASCUNHO PARCIAL: contem apenas os campos mapeados ate agora
-- Abas modeladas neste arquivo:
--   1. Cadastrais > Pessoais
--   2. Fisicos
--   3. Historico > Admissionais
--   4. Historico > Contratuais
--   5. Estrangeiro
--   6. Documentos
--   7. Parentes
--   8. FGTS/GPS
--   9. Vinculos
--   10. Calculo
--   11. Banco
--   12. Dados de partida
--   13. Quadro de horarios
--   14. eSocial > Qualificacao
--   15. eSocial > Integracao
--   16. Outros
-- As demais abas serao adicionadas neste mesmo script nas proximas iteracoes.

BEGIN;

DROP TABLE IF EXISTS public.funcionarios;

CREATE TABLE public.funcionarios (
    -- Chave primaria composta
    registro varchar(14) NOT NULL,
    func_empr integer NOT NULL,
    func_codi integer NOT NULL,
    func_fili integer NOT NULL,

    -- aba Cadastrais > sub-aba Pessoais
    func_admissao_preliminar integer,
    func_integracao_esocial boolean,
    func_nome varchar(200) NOT NULL,
    func_email varchar(200),
    func_ddd varchar(4),
    func_telefone varchar(20),
    func_ddd_celular varchar(4),
    func_celular varchar(20),
    func_nascimento date,
    func_pais_nascimento varchar(7),
    func_cidade_nascimento varchar(60),
    func_naturalidade varchar(2),
    func_grau_instrucao varchar(2),
    func_ficha_registro varchar(20),
    func_livro varchar(20),
    func_folha varchar(20),
    func_cartao_ponto varchar(20),
    func_matricula_esocial varchar(30),
    func_foto_3x4 bytea,

    -- aba Endereco
    func_cep varchar(8),
    func_logr integer,
    func_ende varchar(120),
    func_ende_nume varchar(20),
    func_ende_comp varchar(60),
    func_ende_bair varchar(60),
    func_ende_cida varchar(60),
    func_ende_uf varchar(2),    

    -- aba Fisicos
    func_tipo_sanguineo varchar(5),
    func_etnia_raca integer,
    func_sexo varchar(1),
    func_pessoa_com_deficiencia boolean,
    func_deficiencia_fisica boolean,
    func_deficiencia_visual boolean,
    func_deficiencia_auditiva boolean,
    func_deficiencia_mental boolean,
    func_deficiencia_intelectual boolean,
    func_reabilitado boolean,
    func_cota_deficiencia integer,
    func_observacoes_deficiencias text,

    -- aba Historico > sub-aba Admissionais
    func_admissao date,
    func_cadastro date,
    func_inicio_adicional_tempo_servico date,
    func_alvara_judicial_contratacao_menores boolean,
    func_numero_processo varchar(30),
    func_tipo_admissao integer,
    func_indicativo_admissao integer,
    func_data_aposentadoria date,
    func_nova_data_admissao date,
    func_numero_processo_rt varchar(30),
    func_tipo_provimento integer,
    func_natureza_ocupacao integer,
    func_empresa_anterior_cnpj_cpf varchar(14),
    func_matricula_anterior varchar(30),
    func_data_transferencia date,
    func_transferencia_com_onus boolean,
    func_data_saida date,
    func_aviso_previo date,
    func_motivo_saida text,

    -- aba Historico > sub-aba Contratuais
    func_tipo_contrato_trabalho integer,
    func_indicativo_contratacao text,
    func_prazo_experiencia_dias integer,
    func_fim_primeiro_prazo date,
    func_termino_ocorrencia_fato date,
    func_prorrogacao_dias integer,
    func_fim_prorrogacao date,

    -- aba Estrangeiro
    func_pais_nacionalidade varchar(7),
    func_chegada_brasil date,
    func_casado_brasileiro boolean,
    func_tem_filhos_brasileiros boolean,
    func_rne varchar(20),
    func_orgao_uf_emissao_rne varchar(30),
    func_emissao_rne date,
    func_tempo_residencia integer,
    func_condicao_ingresso integer,

    -- aba Documentos
    func_cpf varchar(11),
    func_pis varchar(14),
    func_emissao_pis date,
    func_rg varchar(20),
    func_orgao_emissor_rg varchar(20),
    func_uf_rg varchar(2),
    func_emissao_rg date,
    func_carteira_trabalho varchar(20),
    func_serie_carteira_trabalho varchar(10),
    func_digito_serie_carteira_trabalho varchar(2),
    func_uf_carteira_trabalho varchar(2),
    func_emissao_carteira_trabalho date,
    func_cnh varchar(20),
    func_categoria_cnh varchar(5),
    func_uf_cnh varchar(2),
    func_emissao_cnh date,
    func_vencimento_cnh date,
    func_primeira_habilitacao date,
    func_titulo_eleitor varchar(20),
    func_zona_titulo_eleitor varchar(5),
    func_secao_titulo_eleitor varchar(5),
    func_certificado_reservista varchar(30),
    func_certidao_civil varchar(30),
    func_tipo_certidao integer,
    func_emissao_certidao date,
    func_termo_matricula varchar(50),
    func_livro_certidao varchar(20),
    func_folha_certidao varchar(20),
    func_cartorio varchar(120),
    func_cidade_cartorio varchar(7),
    func_uf_cartorio varchar(2),

    -- aba Parentes
    func_nome_pai varchar(200),
    func_nome_mae varchar(200),
    func_estado_civil integer,
    func_nome_conjuge varchar(200),
    func_dependentes boolean,

    -- aba FGTS/GPS
    func_data_opcao date,
    func_categoria_sefip integer,
    func_categoria_esocial integer,
    func_grau_risco integer,
    func_percentual_fgts numeric(5,2),
    func_rat_aposentadoria numeric(5,2),
    func_regime_previdenciario integer,
    func_regime_trabalhista integer,
    func_categoria_origem integer,
    func_tipo_origem_inscricao integer,
    func_cnpj_origem varchar(14),
    func_admissao_origem date,
    func_matricula_origem varchar(30),
    func_remuneracao_cargo_eletivo integer,
    func_regime_trabalhista_origem integer,
    func_regime_previdenciario_origem integer,
    func_plano_segregacao integer,
    func_teto_rgps integer,
    func_abono_permanencia integer,
    func_inicio_abono date,

    -- aba Vinculos
    func_classe integer,
    func_sindicato integer,
    func_vinculo_empregaticio integer,
    func_departamento integer,
    func_centro_custo integer,
    func_cargo integer,
    func_nivel integer,
    func_cbo_cargo varchar(10),
    func_funcao integer,
    func_cbo_funcao varchar(10),
    func_acumulacao_cargo integer,
    func_orgao_classe boolean,
    func_inscricao_orgao_classe varchar(30),
    func_orgao_uf_emissao_orgao_classe varchar(30),
    func_emissao_orgao_classe date,
    func_validade_orgao_classe date,

    -- aba Calculo
    func_horas_mes numeric(10,2),
    func_horas_semana numeric(10,2),
    func_horas_dia numeric(10,2),
    func_forma_pagamento integer,
    func_tipo_funcionario integer,
    func_salario_base numeric(15,2),
    func_comissao numeric(5,2),
    func_adic_insalubridade numeric(5,2),
    func_incidencia_insalubridade integer,
    func_adic_periculosidade numeric(5,2),
    func_incidencia_periculosidade integer,
    func_adicional_noturno numeric(5,2),
    func_incidencia_adicional_noturno integer,
    func_vale_alimentacao_compra numeric(15,2),
    func_recebe_dsr_horas_extras boolean,
    func_dsr_horas_extras integer,
    func_recebe_dsr_rendimentos_variaveis boolean,
    func_dsr_rendimentos_variaveis integer,
    func_recebe_dsr_salarios boolean,
    func_dsr_salarios integer,
    func_ignora_faltas_ferias boolean,
    func_imprimir_etiqueta boolean,
    func_regime_tempo_parcial boolean,
    func_nao_arredondar boolean,
    func_salario_contratual_comissionado boolean,
    func_adiantamento boolean,
    func_valor_fixo_adiantamento numeric(15,2),
    func_aplica_deducao_mais_benefica_irrf boolean,
    func_recebe_vale_refeicao boolean,
    func_vale_refeicao integer,
    func_cartao_vale_refeicao varchar(30),
    func_recebe_vale_alimentacao boolean,
    func_vale_alimentacao integer,
    func_cartao_vale_alimentacao varchar(30),

    -- aba Banco
    func_banco varchar(6),
    func_agencia_pagamento varchar(20),
    func_conta_pagamento varchar(30),
    func_digito_conta_pagamento varchar(5),
    func_tipo_conta integer,
    func_cartao_salario varchar(30),
    func_modo_pagamento integer,

    -- aba Dados de partida
    func_aquisicao_ferias date,
    func_salario_inicial numeric(15,2),
    func_descontar_contribuicao_sindical boolean,
    func_sindicalizado boolean,
    func_valor_previdencia_privada numeric(15,2),
    func_valor_previdencia_privada_13 numeric(15,2),
    func_base_ir numeric(15,2),
    func_valor_ir numeric(15,2),
    func_base_inss_multiplos_vinculos numeric(15,2),
    func_valor_inss_multiplos_vinculos numeric(15,2),
    func_base_inss_multiplos_vinculos_13 numeric(15,2),
    func_valor_inss_multiplos_vinculos_13 numeric(15,2),
    func_base_ir_multiplos_vinculos numeric(15,2),
    func_valor_ir_multiplos_vinculos numeric(15,2),
    func_base_ir_multiplos_vinculos_13 numeric(15,2),
    func_valor_ir_multiplos_vinculos_13 numeric(15,2),

    -- aba Quadro de horarios
    func_vigencia_quadro_horario date,
    func_regime_jornada_trabalho integer,
    func_tipo_escala integer,
    func_pre_assinalar_horarios_intervalo boolean,
    func_escala varchar(80),
    func_descanso_semanal integer,
    func_data_inicio_escala date,
    func_tipo_revezamento integer,
    func_tipo_jornada_esocial integer,
    func_horario_noturno boolean,
    func_folga_inicial integer,

    -- aba eSocial > sub-aba Qualificacao
    func_nit varchar(11),
    func_qualificacao_cadastral_status text,

    -- aba eSocial > sub-aba Integracao
    func_esocial_integrado boolean,
    func_esocial_data_integracao timestamp without time zone,
    func_esocial_numero_recibo varchar(40),

    -- aba Outros
    func_ultimo_exame_medico date,
    func_proximo_exame_medico_meses integer,
    func_proximo_exame_medico date,
    func_ultimo_exame_audiometrico date,
    func_proximo_exame_audiometrico_meses integer,
    func_proximo_exame_audiometrico date,
    func_aprendiz_gravida boolean,
    func_observacoes text,

    PRIMARY KEY (registro, func_empr, func_codi, func_fili)
);

COMMENT ON TABLE public.funcionarios IS 'Cadastro de funcionarios por registro, empresa, codigo e filial.';

-- Chave primaria composta
COMMENT ON COLUMN public.funcionarios.registro IS 'Registro da licenca.';
COMMENT ON COLUMN public.funcionarios.func_empr IS 'Codigo da empresa.';
COMMENT ON COLUMN public.funcionarios.func_codi IS 'Codigo do funcionario.';
COMMENT ON COLUMN public.funcionarios.func_fili IS 'Codigo da filial.';

-- aba Cadastrais > sub-aba Pessoais
COMMENT ON COLUMN public.funcionarios.func_admissao_preliminar IS 'Admissao preliminar.';
COMMENT ON COLUMN public.funcionarios.func_integracao_esocial IS 'Integracao eSocial.';
COMMENT ON COLUMN public.funcionarios.func_nome IS 'Nome.';
COMMENT ON COLUMN public.funcionarios.func_email IS 'E-mail.';
COMMENT ON COLUMN public.funcionarios.func_ddd IS 'DDD.';
COMMENT ON COLUMN public.funcionarios.func_telefone IS 'Telefone.';
COMMENT ON COLUMN public.funcionarios.func_ddd_celular IS 'DDD celular.';
COMMENT ON COLUMN public.funcionarios.func_celular IS 'Celular.';
COMMENT ON COLUMN public.funcionarios.func_nascimento IS 'Nascimento.';
COMMENT ON COLUMN public.funcionarios.func_pais_nascimento IS 'Pais de nascimento.';
COMMENT ON COLUMN public.funcionarios.func_cidade_nascimento IS 'Cidade de nascimento.';
COMMENT ON COLUMN public.funcionarios.func_naturalidade IS 'Naturalidade.';
COMMENT ON COLUMN public.funcionarios.func_grau_instrucao IS 'Grau de instrucao.';
COMMENT ON COLUMN public.funcionarios.func_ficha_registro IS 'Ficha registro.';
COMMENT ON COLUMN public.funcionarios.func_livro IS 'Livro.';
COMMENT ON COLUMN public.funcionarios.func_folha IS 'Folha.';
COMMENT ON COLUMN public.funcionarios.func_cartao_ponto IS 'Cartao ponto.';
COMMENT ON COLUMN public.funcionarios.func_matricula_esocial IS 'Matricula eSocial.';
COMMENT ON COLUMN public.funcionarios.func_foto_3x4 IS 'Foto 3x4.';

-- aba Fisicos
COMMENT ON COLUMN public.funcionarios.func_tipo_sanguineo IS 'Tipo sanguineo.';
COMMENT ON COLUMN public.funcionarios.func_etnia_raca IS 'Etnia/Raca.';
COMMENT ON COLUMN public.funcionarios.func_sexo IS 'Sexo.';
COMMENT ON COLUMN public.funcionarios.func_pessoa_com_deficiencia IS 'Pessoa com deficiencia.';
COMMENT ON COLUMN public.funcionarios.func_deficiencia_fisica IS 'Fisica.';
COMMENT ON COLUMN public.funcionarios.func_deficiencia_visual IS 'Visual.';
COMMENT ON COLUMN public.funcionarios.func_deficiencia_auditiva IS 'Auditiva.';
COMMENT ON COLUMN public.funcionarios.func_deficiencia_mental IS 'Mental.';
COMMENT ON COLUMN public.funcionarios.func_deficiencia_intelectual IS 'Intelectual.';
COMMENT ON COLUMN public.funcionarios.func_reabilitado IS 'Reabilitado.';
COMMENT ON COLUMN public.funcionarios.func_cota_deficiencia IS 'Cota deficiencia.';
COMMENT ON COLUMN public.funcionarios.func_observacoes_deficiencias IS 'Observacoes das deficiencias.';

-- aba Historico > sub-aba Admissionais
COMMENT ON COLUMN public.funcionarios.func_admissao IS 'Admissao.';
COMMENT ON COLUMN public.funcionarios.func_cadastro IS 'Cadastro.';
COMMENT ON COLUMN public.funcionarios.func_inicio_adicional_tempo_servico IS 'Inicio adicional tempo de servico.';
COMMENT ON COLUMN public.funcionarios.func_alvara_judicial_contratacao_menores IS 'Alvara judicial (contratacao menores).';
COMMENT ON COLUMN public.funcionarios.func_numero_processo IS 'Numero do processo.';
COMMENT ON COLUMN public.funcionarios.func_tipo_admissao IS 'Tipo de admissao.';
COMMENT ON COLUMN public.funcionarios.func_indicativo_admissao IS 'Indicativo de admissao.';
COMMENT ON COLUMN public.funcionarios.func_data_aposentadoria IS 'Data aposentadoria.';
COMMENT ON COLUMN public.funcionarios.func_nova_data_admissao IS 'Nova data de admissao.';
COMMENT ON COLUMN public.funcionarios.func_numero_processo_rt IS 'Numero do processo RT.';
COMMENT ON COLUMN public.funcionarios.func_tipo_provimento IS 'Tipo de provimento.';
COMMENT ON COLUMN public.funcionarios.func_natureza_ocupacao IS 'Natureza de ocupacao.';
COMMENT ON COLUMN public.funcionarios.func_empresa_anterior_cnpj_cpf IS 'Empresa anterior - CNPJ/CPF.';
COMMENT ON COLUMN public.funcionarios.func_matricula_anterior IS 'Matricula anterior.';
COMMENT ON COLUMN public.funcionarios.func_data_transferencia IS 'Data de transferencia.';
COMMENT ON COLUMN public.funcionarios.func_transferencia_com_onus IS 'Transferencia com onus.';
COMMENT ON COLUMN public.funcionarios.func_data_saida IS 'Data saida.';
COMMENT ON COLUMN public.funcionarios.func_aviso_previo IS 'Aviso previo.';
COMMENT ON COLUMN public.funcionarios.func_motivo_saida IS 'Motivo da saida.';

-- aba Historico > sub-aba Contratuais
COMMENT ON COLUMN public.funcionarios.func_tipo_contrato_trabalho IS 'Tipo de contrato de trabalho.';
COMMENT ON COLUMN public.funcionarios.func_indicativo_contratacao IS 'Indicativo da contratacao.';
COMMENT ON COLUMN public.funcionarios.func_prazo_experiencia_dias IS 'Prazo de experiencia (dias).';
COMMENT ON COLUMN public.funcionarios.func_fim_primeiro_prazo IS 'Fim do 1o prazo.';
COMMENT ON COLUMN public.funcionarios.func_termino_ocorrencia_fato IS 'Termino da ocorrencia de um fato.';
COMMENT ON COLUMN public.funcionarios.func_prorrogacao_dias IS 'Prorrogacao (dias).';
COMMENT ON COLUMN public.funcionarios.func_fim_prorrogacao IS 'Fim da prorrogacao.';

-- aba Estrangeiro
COMMENT ON COLUMN public.funcionarios.func_pais_nacionalidade IS 'Pais de nacionalidade.';
COMMENT ON COLUMN public.funcionarios.func_chegada_brasil IS 'Chegada ao Brasil.';
COMMENT ON COLUMN public.funcionarios.func_casado_brasileiro IS 'Casado com brasileiro(a).';
COMMENT ON COLUMN public.funcionarios.func_tem_filhos_brasileiros IS 'Tem filhos brasileiros.';
COMMENT ON COLUMN public.funcionarios.func_rne IS 'RNE.';
COMMENT ON COLUMN public.funcionarios.func_orgao_uf_emissao_rne IS 'Orgao e UF de emissao.';
COMMENT ON COLUMN public.funcionarios.func_emissao_rne IS 'Emissao.';
COMMENT ON COLUMN public.funcionarios.func_tempo_residencia IS 'Tempo de residencia.';
COMMENT ON COLUMN public.funcionarios.func_condicao_ingresso IS 'Condicao de ingresso.';

-- aba Documentos
COMMENT ON COLUMN public.funcionarios.func_cpf IS 'CPF.';
COMMENT ON COLUMN public.funcionarios.func_pis IS 'PIS.';
COMMENT ON COLUMN public.funcionarios.func_emissao_pis IS 'Emissao PIS.';
COMMENT ON COLUMN public.funcionarios.func_rg IS 'RG.';
COMMENT ON COLUMN public.funcionarios.func_orgao_emissor_rg IS 'Orgao emissor RG.';
COMMENT ON COLUMN public.funcionarios.func_uf_rg IS 'UF RG.';
COMMENT ON COLUMN public.funcionarios.func_emissao_rg IS 'Emissao RG.';
COMMENT ON COLUMN public.funcionarios.func_carteira_trabalho IS 'Carteira de trabalho.';
COMMENT ON COLUMN public.funcionarios.func_serie_carteira_trabalho IS 'Serie.';
COMMENT ON COLUMN public.funcionarios.func_digito_serie_carteira_trabalho IS 'Digito da serie.';
COMMENT ON COLUMN public.funcionarios.func_uf_carteira_trabalho IS 'UF carteira de trabalho.';
COMMENT ON COLUMN public.funcionarios.func_emissao_carteira_trabalho IS 'Emissao carteira de trabalho.';
COMMENT ON COLUMN public.funcionarios.func_cnh IS 'CNH.';
COMMENT ON COLUMN public.funcionarios.func_categoria_cnh IS 'Categoria.';
COMMENT ON COLUMN public.funcionarios.func_uf_cnh IS 'UF CNH.';
COMMENT ON COLUMN public.funcionarios.func_emissao_cnh IS 'Emissao CNH.';
COMMENT ON COLUMN public.funcionarios.func_vencimento_cnh IS 'Vencimento CNH.';
COMMENT ON COLUMN public.funcionarios.func_primeira_habilitacao IS 'Primeira habilitacao.';
COMMENT ON COLUMN public.funcionarios.func_titulo_eleitor IS 'Titulo eleitor.';
COMMENT ON COLUMN public.funcionarios.func_zona_titulo_eleitor IS 'Zona.';
COMMENT ON COLUMN public.funcionarios.func_secao_titulo_eleitor IS 'Secao.';
COMMENT ON COLUMN public.funcionarios.func_certificado_reservista IS 'Certificado de reservista.';
COMMENT ON COLUMN public.funcionarios.func_certidao_civil IS 'Certidao civil.';
COMMENT ON COLUMN public.funcionarios.func_tipo_certidao IS 'Tipo de certidao.';
COMMENT ON COLUMN public.funcionarios.func_emissao_certidao IS 'Emissao certidao.';
COMMENT ON COLUMN public.funcionarios.func_termo_matricula IS 'Termo/Matricula.';
COMMENT ON COLUMN public.funcionarios.func_livro_certidao IS 'Livro.';
COMMENT ON COLUMN public.funcionarios.func_folha_certidao IS 'Folha.';
COMMENT ON COLUMN public.funcionarios.func_cartorio IS 'Cartorio.';
COMMENT ON COLUMN public.funcionarios.func_cidade_cartorio IS 'Cidade.';
COMMENT ON COLUMN public.funcionarios.func_uf_cartorio IS 'UF.';

-- aba Parentes
COMMENT ON COLUMN public.funcionarios.func_nome_pai IS 'Nome do pai.';
COMMENT ON COLUMN public.funcionarios.func_nome_mae IS 'Nome da mae.';
COMMENT ON COLUMN public.funcionarios.func_estado_civil IS 'Estado civil.';
COMMENT ON COLUMN public.funcionarios.func_nome_conjuge IS 'Nome do conjuge.';
COMMENT ON COLUMN public.funcionarios.func_dependentes IS 'Dependentes.';

-- aba FGTS/GPS
COMMENT ON COLUMN public.funcionarios.func_data_opcao IS 'Data opcao.';
COMMENT ON COLUMN public.funcionarios.func_categoria_sefip IS 'Categoria Sefip.';
COMMENT ON COLUMN public.funcionarios.func_categoria_esocial IS 'Categoria eSocial.';
COMMENT ON COLUMN public.funcionarios.func_grau_risco IS 'Grau de risco.';
COMMENT ON COLUMN public.funcionarios.func_percentual_fgts IS 'Percentual FGTS.';
COMMENT ON COLUMN public.funcionarios.func_rat_aposentadoria IS 'RAT aposentadoria (%).';
COMMENT ON COLUMN public.funcionarios.func_regime_previdenciario IS 'Regime previdenciario.';
COMMENT ON COLUMN public.funcionarios.func_regime_trabalhista IS 'Regime trabalhista.';
COMMENT ON COLUMN public.funcionarios.func_categoria_origem IS 'Categoria origem.';
COMMENT ON COLUMN public.funcionarios.func_tipo_origem_inscricao IS 'Tipo.';
COMMENT ON COLUMN public.funcionarios.func_cnpj_origem IS 'CNPJ origem.';
COMMENT ON COLUMN public.funcionarios.func_admissao_origem IS 'Admissao origem.';
COMMENT ON COLUMN public.funcionarios.func_matricula_origem IS 'Matricula origem.';
COMMENT ON COLUMN public.funcionarios.func_remuneracao_cargo_eletivo IS 'Remuneracao cargo eletivo.';
COMMENT ON COLUMN public.funcionarios.func_regime_trabalhista_origem IS 'Regime trabalhista origem.';
COMMENT ON COLUMN public.funcionarios.func_regime_previdenciario_origem IS 'Regime previdenciario origem.';
COMMENT ON COLUMN public.funcionarios.func_plano_segregacao IS 'Plano de segregacao.';
COMMENT ON COLUMN public.funcionarios.func_teto_rgps IS 'Teto RGPS.';
COMMENT ON COLUMN public.funcionarios.func_abono_permanencia IS 'Abono permanencia.';
COMMENT ON COLUMN public.funcionarios.func_inicio_abono IS 'Inicio abono.';

-- aba Vinculos
COMMENT ON COLUMN public.funcionarios.func_classe IS 'Classe.';
COMMENT ON COLUMN public.funcionarios.func_sindicato IS 'Sindicato.';
COMMENT ON COLUMN public.funcionarios.func_vinculo_empregaticio IS 'Vinculo empregaticio.';
COMMENT ON COLUMN public.funcionarios.func_departamento IS 'Departamento.';
COMMENT ON COLUMN public.funcionarios.func_centro_custo IS 'Centro de custo.';
COMMENT ON COLUMN public.funcionarios.func_cargo IS 'Cargo.';
COMMENT ON COLUMN public.funcionarios.func_nivel IS 'Nivel.';
COMMENT ON COLUMN public.funcionarios.func_cbo_cargo IS 'CBO cargo.';
COMMENT ON COLUMN public.funcionarios.func_funcao IS 'Funcao.';
COMMENT ON COLUMN public.funcionarios.func_cbo_funcao IS 'CBO funcao.';
COMMENT ON COLUMN public.funcionarios.func_acumulacao_cargo IS 'Acumulacao de cargo.';
COMMENT ON COLUMN public.funcionarios.func_orgao_classe IS 'Orgao de classe.';
COMMENT ON COLUMN public.funcionarios.func_inscricao_orgao_classe IS 'Inscricao orgao de classe.';
COMMENT ON COLUMN public.funcionarios.func_orgao_uf_emissao_orgao_classe IS 'Orgao e UF de emissao.';
COMMENT ON COLUMN public.funcionarios.func_emissao_orgao_classe IS 'Emissao orgao de classe.';
COMMENT ON COLUMN public.funcionarios.func_validade_orgao_classe IS 'Validade orgao de classe.';

-- aba Calculo
COMMENT ON COLUMN public.funcionarios.func_horas_mes IS 'Horas Men.';
COMMENT ON COLUMN public.funcionarios.func_horas_semana IS 'Horas Sem.';
COMMENT ON COLUMN public.funcionarios.func_horas_dia IS 'Horas Dir.';
COMMENT ON COLUMN public.funcionarios.func_forma_pagamento IS 'Forma de pagamento.';
COMMENT ON COLUMN public.funcionarios.func_tipo_funcionario IS 'Tipo de funcionario.';
COMMENT ON COLUMN public.funcionarios.func_salario_base IS 'Salario base.';
COMMENT ON COLUMN public.funcionarios.func_comissao IS 'Comissao %.';
COMMENT ON COLUMN public.funcionarios.func_adic_insalubridade IS 'Adic. insalubridade %.';
COMMENT ON COLUMN public.funcionarios.func_incidencia_insalubridade IS 'Incidencia insalubridade.';
COMMENT ON COLUMN public.funcionarios.func_adic_periculosidade IS 'Adic. periculosidade %.';
COMMENT ON COLUMN public.funcionarios.func_incidencia_periculosidade IS 'Incidencia periculosidade.';
COMMENT ON COLUMN public.funcionarios.func_adicional_noturno IS 'Adicional noturno %.';
COMMENT ON COLUMN public.funcionarios.func_incidencia_adicional_noturno IS 'Incidencia adicional noturno.';
COMMENT ON COLUMN public.funcionarios.func_vale_alimentacao_compra IS 'Valor de vale alimentacao/compra.';
COMMENT ON COLUMN public.funcionarios.func_recebe_dsr_horas_extras IS 'Recebe DSR sobre horas extras.';
COMMENT ON COLUMN public.funcionarios.func_dsr_horas_extras IS 'DSR H.E.';
COMMENT ON COLUMN public.funcionarios.func_recebe_dsr_rendimentos_variaveis IS 'Recebe DSR sobre rendimentos variaveis.';
COMMENT ON COLUMN public.funcionarios.func_dsr_rendimentos_variaveis IS 'DSR R.V.';
COMMENT ON COLUMN public.funcionarios.func_recebe_dsr_salarios IS 'Recebe DSR sobre salarios.';
COMMENT ON COLUMN public.funcionarios.func_dsr_salarios IS 'DSR salario.';
COMMENT ON COLUMN public.funcionarios.func_ignora_faltas_ferias IS 'Ignora faltas nas ferias.';
COMMENT ON COLUMN public.funcionarios.func_imprimir_etiqueta IS 'Imprimir etiqueta.';
COMMENT ON COLUMN public.funcionarios.func_regime_tempo_parcial IS 'Regime de tempo parcial.';
COMMENT ON COLUMN public.funcionarios.func_nao_arredondar IS 'Nao arredondar.';
COMMENT ON COLUMN public.funcionarios.func_salario_contratual_comissionado IS 'Salario contratual comissionado.';
COMMENT ON COLUMN public.funcionarios.func_adiantamento IS 'Adiantamento.';
COMMENT ON COLUMN public.funcionarios.func_valor_fixo_adiantamento IS 'Valor fixo.';
COMMENT ON COLUMN public.funcionarios.func_aplica_deducao_mais_benefica_irrf IS 'Aplica deducao mais benefica no IRRF.';
COMMENT ON COLUMN public.funcionarios.func_recebe_vale_refeicao IS 'Recebe vale refeicao.';
COMMENT ON COLUMN public.funcionarios.func_vale_refeicao IS 'Vale refeicao.';
COMMENT ON COLUMN public.funcionarios.func_cartao_vale_refeicao IS 'Cartao vale refeicao.';
COMMENT ON COLUMN public.funcionarios.func_recebe_vale_alimentacao IS 'Recebe vale alimentacao.';
COMMENT ON COLUMN public.funcionarios.func_vale_alimentacao IS 'Vale alimentacao.';
COMMENT ON COLUMN public.funcionarios.func_cartao_vale_alimentacao IS 'Cartao vale alimentacao.';

-- aba Banco
COMMENT ON COLUMN public.funcionarios.func_banco IS 'Banco.';
COMMENT ON COLUMN public.funcionarios.func_agencia_pagamento IS 'Agencia para pagamento.';
COMMENT ON COLUMN public.funcionarios.func_conta_pagamento IS 'Conta deposito para pagamento.';
COMMENT ON COLUMN public.funcionarios.func_digito_conta_pagamento IS 'Digito da conta para pagamento.';
COMMENT ON COLUMN public.funcionarios.func_tipo_conta IS 'Tipo de conta.';
COMMENT ON COLUMN public.funcionarios.func_cartao_salario IS 'Cartao salario.';
COMMENT ON COLUMN public.funcionarios.func_modo_pagamento IS 'Modo de pagamento.';

-- aba Dados de partida
COMMENT ON COLUMN public.funcionarios.func_aquisicao_ferias IS 'Aquisicao ferias.';
COMMENT ON COLUMN public.funcionarios.func_salario_inicial IS 'Salario inicial.';
COMMENT ON COLUMN public.funcionarios.func_descontar_contribuicao_sindical IS 'Descontar contribuicao sindical.';
COMMENT ON COLUMN public.funcionarios.func_sindicalizado IS 'Sindicalizado.';
COMMENT ON COLUMN public.funcionarios.func_valor_previdencia_privada IS 'Valor previdencia privada.';
COMMENT ON COLUMN public.funcionarios.func_valor_previdencia_privada_13 IS 'Valor previdencia privada 13.';
COMMENT ON COLUMN public.funcionarios.func_base_ir IS 'Base de IR.';
COMMENT ON COLUMN public.funcionarios.func_valor_ir IS 'Valor de IR.';
COMMENT ON COLUMN public.funcionarios.func_base_inss_multiplos_vinculos IS 'Base de INSS multiplos vinculos.';
COMMENT ON COLUMN public.funcionarios.func_valor_inss_multiplos_vinculos IS 'Valor de INSS multiplos vinculos.';
COMMENT ON COLUMN public.funcionarios.func_base_inss_multiplos_vinculos_13 IS 'Base de INSS multiplos vinculos 13.';
COMMENT ON COLUMN public.funcionarios.func_valor_inss_multiplos_vinculos_13 IS 'Valor de INSS multiplos vinculos 13.';
COMMENT ON COLUMN public.funcionarios.func_base_ir_multiplos_vinculos IS 'Base de IR multiplos vinculos.';
COMMENT ON COLUMN public.funcionarios.func_valor_ir_multiplos_vinculos IS 'Valor de IR multiplos vinculos.';
COMMENT ON COLUMN public.funcionarios.func_base_ir_multiplos_vinculos_13 IS 'Base de IR multiplos vinculos 13.';
COMMENT ON COLUMN public.funcionarios.func_valor_ir_multiplos_vinculos_13 IS 'Valor de IR multiplos vinculos 13.';

-- aba Quadro de horarios
COMMENT ON COLUMN public.funcionarios.func_vigencia_quadro_horario IS 'Vigencia.';
COMMENT ON COLUMN public.funcionarios.func_regime_jornada_trabalho IS 'Regime jornada de trabalho.';
COMMENT ON COLUMN public.funcionarios.func_tipo_escala IS 'Tipo de escala.';
COMMENT ON COLUMN public.funcionarios.func_pre_assinalar_horarios_intervalo IS 'Pre assinalar horarios de intervalo.';
COMMENT ON COLUMN public.funcionarios.func_escala IS 'Escala.';
COMMENT ON COLUMN public.funcionarios.func_descanso_semanal IS 'Descanso semanal.';
COMMENT ON COLUMN public.funcionarios.func_data_inicio_escala IS 'Data inicio escala.';
COMMENT ON COLUMN public.funcionarios.func_tipo_revezamento IS 'Tipo de revezamento.';
COMMENT ON COLUMN public.funcionarios.func_tipo_jornada_esocial IS 'Tipo de jornada eSocial (Tabela 7 eSocial - 0=Nao informado, 1=Diario fixo, 2=Fixo folga variavel, 3=Fixo folga fixa outro dia, 4=Fixo folga fixa domingo, 5=Turno ininterrupto revezamento, 6=12x36, 9=Demais).';
COMMENT ON COLUMN public.funcionarios.func_horario_noturno IS 'Horario noturno.';
COMMENT ON COLUMN public.funcionarios.func_folga_inicial IS 'Folga inicial.';

-- aba eSocial > sub-aba Qualificacao
COMMENT ON COLUMN public.funcionarios.func_nit IS 'NIT.';
COMMENT ON COLUMN public.funcionarios.func_qualificacao_cadastral_status IS 'Status da qualificacao cadastral.';

-- aba eSocial > sub-aba Integracao
COMMENT ON COLUMN public.funcionarios.func_esocial_integrado IS 'Integrado no eSocial.';
COMMENT ON COLUMN public.funcionarios.func_esocial_data_integracao IS 'Data e hora da integracao no eSocial.';
COMMENT ON COLUMN public.funcionarios.func_esocial_numero_recibo IS 'Numero do recibo.';

-- aba Outros
COMMENT ON COLUMN public.funcionarios.func_ultimo_exame_medico IS 'Ultimo exame medico.';
COMMENT ON COLUMN public.funcionarios.func_proximo_exame_medico_meses IS 'Proximo exame (meses) - medico.';
COMMENT ON COLUMN public.funcionarios.func_proximo_exame_medico IS 'Proximo exame medico.';
COMMENT ON COLUMN public.funcionarios.func_ultimo_exame_audiometrico IS 'Ultimo exame audiometrico.';
COMMENT ON COLUMN public.funcionarios.func_proximo_exame_audiometrico_meses IS 'Proximo exame (meses) - audiometrico.';
COMMENT ON COLUMN public.funcionarios.func_proximo_exame_audiometrico IS 'Proximo exame audiometrico.';
COMMENT ON COLUMN public.funcionarios.func_aprendiz_gravida IS 'Aprendiz gravida.';
COMMENT ON COLUMN public.funcionarios.func_observacoes IS 'Observacoes.';

COMMIT;
