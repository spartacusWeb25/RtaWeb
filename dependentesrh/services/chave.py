from django.db.models import Max
from django.db.models.functions import Coalesce


class DependentesChaveService:
    CAMPOS_CHAVE = [
        "registro",
        "depe_empr",
        "depe_fili",
        "depe_func",
        "depe_codi",
    ]

    @staticmethod
    def montar_chave(*, banco, dados):
        return {
            "registro": banco,
            "depe_empr": dados.get("depe_empr"),
            "depe_fili": dados.get("depe_fili"),
            "depe_func": dados.get("depe_func"),
            "depe_codi": dados.get("depe_codi"),
        }

    @staticmethod
    def existe(*, banco, db_alias, dados):
        from dependentesrh.models import Dependentesrh

        chave = DependentesChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return False

        return Dependentesrh.objects.using(db_alias).filter(**chave).exists()

    @staticmethod
    def buscar(*, banco, db_alias, dados):
        from dependentesrh.models import Dependentesrh

        chave = DependentesChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return None

        return Dependentesrh.objects.using(db_alias).filter(**chave).first()

    @staticmethod
    def remover(*, banco, db_alias, dados):
        from dependentesrh.models import Dependentesrh

        chave = DependentesChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return

        Dependentesrh.objects.using(db_alias).filter(**chave).delete()

    @staticmethod
    def proximo_codigo(*, banco, db_alias, empresa, filial, funcionario):
        from dependentesrh.models import Dependentesrh

        return (
            Dependentesrh.objects.using(db_alias)
            .filter(
                registro=banco,
                depe_empr=empresa,
                depe_fili=filial,
                depe_func=funcionario,
            )
            .aggregate(proximo=Coalesce(Max("depe_codi"), 0) + 1)["proximo"]
        )
