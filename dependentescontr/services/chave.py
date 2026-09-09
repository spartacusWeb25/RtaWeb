from django.db.models import Max
from django.db.models.functions import Coalesce


class DependentescontrChaveService:
    CAMPOS_CHAVE = [
        "registro",
        "depecontr_empr",
        "depecontr_fili",
        "depecontr_contr",
        "depecontr_codi",
    ]

    @staticmethod
    def montar_chave(*, banco, dados):
        return {
            "registro": banco,
            "depecontr_empr": dados.get("depecontr_empr"),
            "depecontr_fili": dados.get("depecontr_fili"),
            "depecontr_contr": dados.get("depecontr_contr"),
            "depecontr_codi": dados.get("depecontr_codi"),
        }

    @staticmethod
    def existe(*, banco, db_alias, dados):
        from dependentescontr.models import Dependentescontr

        chave = DependentescontrChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return False

        return Dependentescontr.objects.using(db_alias).filter(**chave).exists()

    @staticmethod
    def buscar(*, banco, db_alias, dados):
        from dependentescontr.models import Dependentescontr

        chave = DependentescontrChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return None

        return Dependentescontr.objects.using(db_alias).filter(**chave).first()

    @staticmethod
    def remover(*, banco, db_alias, dados):
        from dependentescontr.models import Dependentescontr

        chave = DependentescontrChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return

        Dependentescontr.objects.using(db_alias).filter(**chave).delete()

    @staticmethod
    def proximo_codigo(*, banco, db_alias, empresa, filial, contribuinte):
        from dependentescontr.models import Dependentescontr

        return (
            Dependentescontr.objects.using(db_alias)
            .filter(
                registro=banco,
                depecontr_empr=empresa,
                depecontr_fili=filial,
                depecontr_contr=contribuinte,
            )
            .aggregate(proximo=Coalesce(Max("depecontr_codi"), 0) + 1)["proximo"]
        )
