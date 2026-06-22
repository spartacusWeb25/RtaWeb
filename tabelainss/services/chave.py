class TabelaInssChaveService:
    CAMPOS_CHAVE = [
        "tabe_refe",
    ]

    @staticmethod
    def montar_chave(*, banco, dados):
        return {
            "tabe_refe": dados.get("tabe_refe"),
        }

    @staticmethod
    def existe(*, banco, db_alias, dados):
        from tabelainss.models import Tabelainss

        chave = TabelaInssChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return False

        return Tabelainss.objects.using(db_alias).filter(**chave).exists()

    @staticmethod
    def buscar(*, banco, db_alias, dados):
        from tabelainss.models import Tabelainss

        chave = TabelaInssChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return None

        return Tabelainss.objects.using(db_alias).filter(**chave).first()
   
    @staticmethod
    def remover(*, banco, db_alias, dados):
        from tabelainss.models import Tabelainss

        chave = TabelaInssChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return

        Tabelainss.objects.using(db_alias).filter(**chave).delete()

    
