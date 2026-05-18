from django.http import Http404
from folhamensal.models import Folhamensal


class FolhaMensalRemoverService:
    @staticmethod
    def buscar_por_chave(
        *,
        banco,
        db_alias,
        fome_empr,
        fome_fili,
        fome_func,
        fome_refe,
        fome_even,
    ):
        obj = Folhamensal.objects.using(db_alias).filter(
            registro=banco,
            fome_empr=fome_empr,
            fome_fili=fome_fili,
            fome_func=fome_func,
            fome_refe=fome_refe,
            fome_even=fome_even,
        ).first()

        if not obj:
            raise Http404("Lançamento não encontrado.")

        return obj

    @staticmethod
    def remover_por_chave(
        *,
        banco,
        db_alias,
        fome_empr,
        fome_fili,
        fome_func,
        fome_refe,
        fome_even,
    ):
        qs = Folhamensal.objects.using(db_alias).filter(
            registro=banco,
            fome_empr=fome_empr,
            fome_fili=fome_fili,
            fome_func=fome_func,
            fome_refe=fome_refe,
            fome_even=fome_even,
        )

        total = qs.count()

        if total != 1:
            raise Http404("Lançamento não encontrado ou chave ambígua.")

        qs.delete()