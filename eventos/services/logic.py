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
