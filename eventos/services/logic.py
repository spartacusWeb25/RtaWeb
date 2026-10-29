from django.shortcuts import get_object_or_404

from eventos.models import Eventos


class EventosService:

    @staticmethod
    def listar_por_banco(*, banco: str, termo: str = None):
        qs = Eventos.objects.filter(registro=banco)
        if termo:
            qs = qs.filter(even_desc__icontains=termo)
        return qs.order_by("even_codi")

    @staticmethod
    def buscar(*, banco: str, even_empr: int, even_codi: int):
        return Eventos.objects.filter(
            registro=banco,
            even_empr=even_empr,
            even_codi=even_codi,
        ).first()

    @staticmethod
    def buscar_ou_404(*, banco: str, even_empr: int, even_codi: int):
        return get_object_or_404(
            Eventos.objects,
            registro=banco,
            even_empr=even_empr,
            even_codi=even_codi,
        )

    @staticmethod
    def salvar_form(*, banco: str, even_empr: int, db_alias: str = None, form) -> Eventos:
        instance = form.save(commit=False)
        instance.registro = banco
        instance.even_empr = even_empr
        if db_alias:
            instance.save(using=db_alias)
        else:
            instance.save()
        return instance

    @staticmethod
    def remover(*, banco: str, instance: Eventos) -> None:
        instance.delete()

    @staticmethod
    def obter_empresa_padrao(*, banco: str, db_alias: str = None):
        from empresas.models import Empresas
        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        return (
            qs.filter(registro=banco)
            .order_by("empr_empr", "empr_fili", "empr_nome")
            .first()
        )

    @staticmethod
    def obter_nome_empresa(*, banco: str, db_alias: str = None, codigo_empresa=None) -> str:
        if not codigo_empresa:
            return ""

        from empresas.models import Empresas

        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        empresa = (
            qs.filter(registro=banco, empr_empr=codigo_empresa)
            .order_by("empr_fili", "empr_nome")
            .first()
        )
        return getattr(empresa, "empr_nome", "") or ""

    @staticmethod
    def obter_filial_padrao(*, banco: str, db_alias: str = None, codigo_empresa=None):
        from empresas.models import Empresas

        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        filtros = {"registro": banco}
        if codigo_empresa not in (None, ""):
            filtros["empr_empr"] = codigo_empresa

        return (
            qs.filter(**filtros)
            .order_by("empr_empr", "empr_fili", "empr_nome")
            .first()
        )

    @staticmethod
    def obter_nome_filial(*, banco: str, db_alias: str = None, codigo_empresa=None, codigo_filial=None) -> str:
        if not codigo_empresa or not codigo_filial:
            return ""

        from empresas.models import Empresas

        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        filial = (
            qs.filter(registro=banco, empr_empr=codigo_empresa, empr_fili=codigo_filial)
            .order_by("empr_fili", "empr_nome")
            .first()
        )
        return getattr(filial, "empr_fant", "") or getattr(filial, "empr_nome", "") or ""
