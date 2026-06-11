class TabelaSalaFamiChaveService:
    CAMPOS_CHAVE = [
        "safa_refe",
    ]

    @staticmethod
    def montar_chave(*, banco, dados):
        return {
            "safa_refe": dados.get("safa_refe"),
        }

    @staticmethod
    def existe(*, banco, db_alias, dados):
        from tabelasalafami.models import Tabelasalafami

        chave = TabelaSalaFamiChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return False

        return Tabelasalafami.objects.using(db_alias).filter(**chave).exists()

    @staticmethod
    def buscar(*, banco, db_alias, dados):
        from tabelasalafami.models import Tabelasalafami

        chave = TabelaSalaFamiChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return None

        return Tabelasalafami.objects.using(db_alias).filter(**chave).first()
   
    @staticmethod
    def remover(*, banco, db_alias, dados):
        from tabelasalafami.models import Tabelasalafami

        chave = TabelaSalaFamiChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return

        Tabelasalafami.objects.using(db_alias).filter(**chave).delete()

    
