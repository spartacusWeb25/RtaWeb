from django.db.models import Max
from django.db.models.functions import Coalesce


class DependentestercChaveService:
    CAMPOS_CHAVE = [
        "registro",
        "depe_empr",
        "depe_fili",
        "depe_terc",
        "depe_codi",
    ]

    @staticmethod
    def montar_chave(*, banco, dados):
        return {
            "registro": banco,
            "depe_empr": dados.get("depe_empr") or dados.get("empr") or dados.get("empresa"),
            "depe_fili": dados.get("depe_fili") or dados.get("fili") or dados.get("filial"),
            "depe_terc": dados.get("depe_terc") or dados.get("terc") or dados.get("terceiro"),
            "depe_codi": dados.get("depe_codi") or dados.get("codi"),
        }

    @staticmethod
    def existe(*, banco, db_alias, dados):
        from dependentesterc.models import Dependentesterc

        chave = DependentestercChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return False

        return Dependentesterc.objects.using(db_alias).filter(**chave).exists()

    @staticmethod
    def buscar(*, banco, db_alias, dados):
        from dependentesterc.models import Dependentesterc

        chave = DependentestercChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return None

        return Dependentesterc.objects.using(db_alias).filter(**chave).first()

    @staticmethod
    def remover(*, banco, db_alias, dados):
        from dependentesterc.models import Dependentesterc

        chave = DependentestercChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return

        Dependentesterc.objects.using(db_alias).filter(**chave).delete()

    @staticmethod
    def proximo_codigo(*, banco, db_alias, empresa, filial, terceiro):
        from dependentesterc.models import Dependentesterc

        return (
            Dependentesterc.objects.using(db_alias)
            .filter(
                registro=banco,
                depe_empr=empresa,
                depe_fili=filial,
                depe_terc=terceiro,
            )
            .aggregate(proximo=Coalesce(Max("depe_codi"), 0) + 1)["proximo"]
        )
