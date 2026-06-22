from tabelasalariominimo.services.chave import TabelaSalarioMinimoChaveService



class TabelaSalarioMinimoCriarService:
    def __init__(self, chave_service):
        self.chave_service = chave_service
    
    @staticmethod
    def criar(*, banco, db_alias, dados):
        from tabelasalariominimo.models import Tabelasalariominimo

        dados = dict(dados)
        chave = TabelaSalarioMinimoChaveService.montar_chave(banco=banco, dados=dados)

        if not all(chave.values()):
            return

        return Tabelasalariominimo.objects.using(db_alias).create(**dados)
