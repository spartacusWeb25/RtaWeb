from tabelairrf.services.chave import TabelaIrrfChaveService


class TabelaIrrfCriarService:
    def __init__(self, chave_service):
        self.chave_service = chave_service

    @staticmethod
    def criar(*, banco, db_alias, dados):
        from tabelairrf.models import Tabelairrf

        dados = dict(dados)
        chave = TabelaIrrfChaveService.montar_chave(banco=banco, dados=dados)

        if not all(chave.values()):
            return

        return Tabelairrf.objects.using(db_alias).create(**dados)
