ABA_CAMPOS = {
    "cadastrais": [
        "depecontr_empr",
        "depecontr_fili",
        "depecontr_contr",
        "depecontr_codi",
        "depecontr_nome",
        "depecontr_nascimento",
        "depecontr_cpf",
        "depecontr_matricula",
        "depecontr_local_nascimento",
        "depecontr_tipo_dependente",
        "depecontr_tipo_dependencia",
        "depecontr_desc_dependencia",
        "depecontr_grau_parentesco",
        "depecontr_invalido",
        "depecontr_dependente_irrf",
        "depecontr_dependente_salario_familia",
    ],
    "documentos": [
        "depecontr_rg",
        "depecontr_orgao_emissor_rg",
        "depecontr_uf_rg",
        "depecontr_emissao_rg",
        "depecontr_certidao_nascimento",
        "depecontr_cartorio",
        "depecontr_numero_registro",
        "depecontr_numero_livro",
        "depecontr_numero_folha",
        "depecontr_data_entrega",
        "depecontr_cidade_codigo",
        "depecontr_cidade",
    ],
    "pensao": [
        "depecontr_pensao_alimenticia_valor",
        "depecontr_pensao_alimenticia_percentual",
        "depecontr_data_baixa",
        "depecontr_ir_ate",
        "depecontr_observacoes",
    ],
}


def _has_errors(form) -> dict:
    campos_com_erro = set(form.errors.keys())
    return {
        aba: bool(campos_com_erro & set(campos))
        for aba, campos in ABA_CAMPOS.items()
    }
