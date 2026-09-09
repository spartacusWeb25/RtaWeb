from dependentescontr.services.chave import DependentescontrChaveService


def _sanitizar_valor(campo, valor, model_cls):
    try:
        field = model_cls._meta.get_field(campo)
    except Exception:
        return valor
    import django.db.models as dm
    is_integer = isinstance(field, (dm.IntegerField, dm.BigIntegerField, dm.SmallIntegerField, dm.PositiveIntegerField, dm.PositiveSmallIntegerField))
    is_boolean = isinstance(field, dm.BooleanField)
    is_decimal = isinstance(field, dm.DecimalField)
    if is_integer:
        if valor in (None, '', []):
            return field.null and None or 0
        if isinstance(valor, bool):
            return 1 if valor else 0
        if isinstance(valor, int):
            return valor
        s = str(valor).strip()
        if not s:
            return field.null and None or 0
        if s.lstrip('-').isdigit():
            try:
                return int(s)
            except Exception:
                return field.null and None or 0
        return field.null and None or 0
    if is_boolean:
        if valor in (None, '', []):
            return bool(field.default) if field.has_default() else False
        if isinstance(valor, bool):
            return valor
        return str(valor).strip().lower() not in ('0', 'false', 'no', 'não', 'nao', '')
    if is_decimal:
        if valor in (None, '', []):
            return None
        if isinstance(valor, (int, float)):
            return valor
        s = str(valor).strip().replace(',', '.')
        try:
            return float(s)
        except Exception:
            return None
    return valor


class DependentescontrCriarService:
    def __init__(self, chave_service):
        self.chave_service = chave_service

    @staticmethod
    def criar(*, banco, db_alias, dados):
        from dependentescontr.models import Dependentescontr

        chave = DependentescontrChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return

        campos_chave = set(DependentescontrChaveService.CAMPOS_CHAVE)
        dados_limpos = {}
        todos_campos = {f.name for f in Dependentescontr._meta.get_fields()}
        for campo, valor in dados.items():
            if campo not in todos_campos or campo in campos_chave:
                continue
            dados_limpos[campo] = _sanitizar_valor(campo, valor, Dependentescontr)

        for campo in campos_chave:
            if campo in chave and chave[campo] is not None:
                chave[campo] = _sanitizar_valor(campo, chave[campo], Dependentescontr)

        return Dependentescontr.objects.using(db_alias).create(
            **chave,
            **dados_limpos,
        )
