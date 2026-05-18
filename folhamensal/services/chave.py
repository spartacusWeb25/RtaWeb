# folhamensal/services/chave.py

class FolhaMensalChaveService:
    CAMPOS_CHAVE = [
        "registro",
        "fome_empr",
        "fome_fili",
        "fome_func",
        "fome_refe",
        "fome_even",
    ]

    @staticmethod
    def montar(*, banco, dados):
        return {
            "registro": banco,
            "fome_empr": dados.get("fome_empr"),
            "fome_fili": dados.get("fome_fili"),
            "fome_func": dados.get("fome_func"),
            "fome_refe": dados.get("fome_refe"),
            "fome_even": dados.get("fome_even"),
        }

    @staticmethod
    def existe(*, banco, db_alias, dados):
        from folhamensal.models import Folhamensal

        chave = FolhaMensalChaveService.montar(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return False

        return Folhamensal.objects.using(db_alias).filter(**chave).exists()