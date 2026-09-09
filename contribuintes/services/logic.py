from django.core.exceptions import ValidationError
from empresas.models import Empresas
from contribuintes.models import Contribuintes


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


class ContribuintesService:

    @staticmethod
    def salvar_form(form, banco, db_alias, contr_empr=None, contr_fili=None, **kwargs):
        instance = form.save(commit=False)
        instance.registro = _digits_only(banco)
        if contr_empr is not None:
            instance.contr_empr = contr_empr
        if contr_fili is not None:
            instance.contr_fili = contr_fili

        for binary_field_name in ["contr_foto_3x4", "contr_carteira_identidade_arquivo"]:
            uploaded = form.cleaned_data.get(binary_field_name) if form.is_bound else None
            if uploaded and hasattr(uploaded, "read"):
                setattr(instance, binary_field_name, uploaded.read())

        instance.save(using=db_alias)
        return instance

    @staticmethod
    def excluir_contribuinte(instance, db_alias):
        instance.delete(using=db_alias)

    @staticmethod
    def obter_nome_empresa(*, banco: str, db_alias: str = None, codigo_empresa=None) -> str:
        if not codigo_empresa:
            return ""

        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        empresa = (
            qs.filter(registro=_digits_only(banco), empr_empr=codigo_empresa)
            .order_by("empr_fili", "empr_nome")
            .first()
        )
        return getattr(empresa, "empr_nome", "") or ""

    @staticmethod
    def obter_nome_filial(*, banco: str, db_alias: str = None, codigo_empresa=None, codigo_filial=None) -> str:
        if not codigo_empresa or not codigo_filial:
            return ""

        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        filial = (
            qs.filter(registro=_digits_only(banco), empr_empr=codigo_empresa, empr_fili=codigo_filial)
            .order_by("empr_fili")
            .first()
        )
        descricao = getattr(filial, "empr_fant", "") or getattr(filial, "empr_nome", "") or ""
        if not descricao and codigo_filial == 1:
            return ""
        if not descricao:
            return f"Filial {codigo_filial} - Matriz" if codigo_filial == 1 else f"Filial {codigo_filial}"
        return f"Filial {codigo_filial} - {descricao}"

    @staticmethod
    def obter_empresa_padrao(*, banco: str, db_alias: str = None):
        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        return (
            qs.filter(registro=_digits_only(banco))
            .order_by("empr_empr", "empr_fili", "empr_nome")
            .first()
        )

    @staticmethod
    def obter_filial_padrao(*, banco: str, db_alias: str = None):
        return ContribuintesService.obter_empresa_padrao(banco=banco, db_alias=db_alias)
