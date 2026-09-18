ABA_CAMPOS = {
    "cadastrais": [
        "terc_empr",
        "terc_fili",
        "terc_codi",
        "terc_nome",
    ],
}


def _has_errors(form) -> dict:
    campos_com_erro = set(form.errors.keys())
    return {
        aba: bool(campos_com_erro & set(campos))
        for aba, campos in ABA_CAMPOS.items()
    }
