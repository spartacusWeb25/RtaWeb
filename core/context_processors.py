from empresas.models import Empresas


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _formatar_documento(value):
    digits = _digits_only(value)
    if len(digits) == 11:
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
    if len(digits) == 14:
        return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
    return digits or str(value or "")


def statusbar_context(request):
    registro = getattr(request, "banco", None) or request.session.get("registro") or ""
    registro_digits = _digits_only(registro)
    db_alias = getattr(request, "db_alias", None) or "default"

    empresa_codigo = getattr(request, "empr_padrao_cod", None) or 1
    filial_codigo = getattr(request, "fili_padrao_cod", None) or 1
    empresa_nome = ""

    try:
        empresa = (
            Empresas.objects.using(db_alias)
            .filter(
                registro=registro_digits,
                empr_empr=int(empresa_codigo),
                empr_fili=int(filial_codigo),
            )
            .only("empr_nome")
            .first()
        )
        empresa_nome = getattr(empresa, "empr_nome", "") or ""
    except Exception:
        empresa_nome = ""

    if not empresa_nome:
        try:
            empresa = (
                Empresas.objects.using(db_alias)
                .filter(
                    registro=registro_digits,
                    empr_empr=int(empresa_codigo),
                )
                .only("empr_nome")
                .order_by("empr_fili", "empr_nome")
                .first()
            )
            empresa_nome = getattr(empresa, "empr_nome", "") or ""
        except Exception:
            empresa_nome = ""

    if not empresa_nome:
        empresa_nome = request.session.get("licenca_nome") or ""

    empresa_display = str(empresa_codigo or "-")
    if empresa_nome:
        empresa_display = f"{empresa_codigo} - {empresa_nome}"

    return {
        "statusbar_licenca": _formatar_documento(registro_digits or registro),
        "statusbar_empresa": empresa_display,
        "statusbar_filial": str(filial_codigo or "-"),
    }
