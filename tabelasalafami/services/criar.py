from tabelasalafami.services.chave import TabelaSalaFamiChaveService



class SalaFamiCriarService:
    def __init__(self, chave_service):
        self.chave_service = chave_service
    
    @staticmethod
    def criar(*, banco, db_alias, dados):
        from tabelasalafami.models import Tabelasalafami

        dados = dict(dados)
        chave = TabelaSalaFamiChaveService.montar_chave(banco=banco, dados=dados)

        if not all(chave.values()):
            return

        return Tabelasalafami.objects.using(db_alias).create(**dados)
