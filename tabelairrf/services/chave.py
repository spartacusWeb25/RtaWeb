class TabelaIrrfChaveService:
    CAMPOS_CHAVE = [
        "irrf_refe",
    ]

    @staticmethod
    def montar_chave(*, banco, dados):
        return {
            "irrf_refe": dados.get("irrf_refe"),
        }

    @staticmethod
    def existe(*, banco, db_alias, dados):
        from tabelairrf.models import Tabelairrf

        chave = TabelaIrrfChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return False

        return Tabelairrf.objects.using(db_alias).filter(**chave).exists()

    @staticmethod
    def buscar(*, banco, db_alias, dados):
        from tabelairrf.models import Tabelairrf

        chave = TabelaIrrfChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return None

        return Tabelairrf.objects.using(db_alias).filter(**chave).first()

    @staticmethod
    def remover(*, banco, db_alias, dados):
        from tabelairrf.models import Tabelairrf

        chave = TabelaIrrfChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return

        Tabelairrf.objects.using(db_alias).filter(**chave).delete()
