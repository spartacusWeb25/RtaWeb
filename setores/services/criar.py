from setores.services.chave import SetoresChaveService



class SetoresCriarService:
    def __init__(self, chave_service):
        self.chave_service = chave_service
    
    @staticmethod
    def criar(*, banco, db_alias, dados):
        from setores.models import Setoresrh

        chave = SetoresChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return

        Setoresrh.objects.using(db_alias).create(
            **chave,
        )