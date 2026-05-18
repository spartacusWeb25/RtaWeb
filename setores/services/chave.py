
class SetoresChaveService:
    CAMPOS_CHAVE = [
        "registro",
        "seto_empr",
        "seto_codi",
    ]

    @staticmethod
    def montar_chave(*, banco, dados):
        return {
            "registro": banco,
            "seto_empr": dados.get("seto_empr"),
            "seto_codi": dados.get("seto_codi"),
        }

    @staticmethod
    def existe(*, banco, db_alias, dados):
        from setores.models import Setoresrh

        chave = SetoresChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return False

        return Setoresrh.objects.using(db_alias).filter(**chave).exists()   
    @staticmethod
    def buscar(*, banco, db_alias, dados):
        from setores.models import Setoresrh

        chave = SetoresChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return None

        return Setoresrh.objects.using(db_alias).filter(**chave).first()
   
    @staticmethod
    def remover(*, banco, db_alias, dados):
        from setores.models import Setoresrh

        chave = SetoresChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return

        Setoresrh.objects.using(db_alias).filter(**chave).delete()
    
