from django.http import Http404

from folhamensal.models import Folhamensal


class FolhaMensalSalvarService:
    def criar(*, banco, db_alias, dados):
        dados = dict(dados)

        # blindagem: registro SEMPRE vem da request, nunca do form
        dados.pop("registro", None)

        return Folhamensal.objects.using(db_alias).create(
            registro=banco,
            **dados
        )


class FolhaMensalRemoverService:
    @staticmethod
    def remover(*, instance: Folhamensal, db_alias: str) -> None:
        instance.delete(using=db_alias)


class FolhaMensalEditarService:
    @staticmethod
    def buscar_unico(
        *,
        banco: str,
        db_alias: str,
        fome_empr: int,
        fome_fili: int,
        fome_func: int,
        fome_refe: str,
        fome_even: int,
    ) -> Folhamensal:
        obj = (
            Folhamensal.objects.using(db_alias)
            .filter(
                registro=banco,
                fome_empr=fome_empr,
                fome_fili=fome_fili,
                fome_func=fome_func,
                fome_refe=fome_refe,
                fome_even=fome_even,
            )
            .first()
        )
        if obj is None:
            raise Http404("Lançamento não encontrado.")
        return obj

    @staticmethod
    def editar(*, instance: Folhamensal, db_alias: str) -> Folhamensal:
        instance.save(using=db_alias)
        return instance
