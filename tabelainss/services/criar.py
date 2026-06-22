from tabelainss.services.chave import TabelaInssChaveService



class TabelaInssCriarService:
    def __init__(self, chave_service):
        self.chave_service = chave_service
    
    @staticmethod
    def criar(*, banco, db_alias, dados):
        from tabelainss.models import Tabelainss

        dados = dict(dados)
        chave = TabelaInssChaveService.montar_chave(banco=banco, dados=dados)

        if not all(chave.values()):
            return

        return Tabelainss.objects.using(db_alias).create(**dados)
