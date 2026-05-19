from setores.models import Setoresrh
from setores.services.chave import SetoresChaveService


class SetoresEditarService:

    @staticmethod
    def editar(*, banco, db_alias, dados):
        setor = SetoresChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not setor:
            raise ValueError("Setor não encontrado.")

        setor.seto_desc = dados.get("seto_desc")
        setor.save(using=db_alias)

        return setor