from empresas.services.chave import EmpresasChaveService



class EmpresasCriarService:
    def __init__(self, chave_service):
        self.chave_service = chave_service
    
    @staticmethod
    def criar(*, banco, db_alias, dados):
        from empresas.models import Empresas

        dados = dict(dados)
        chave = EmpresasChaveService.montar_chave(banco=banco, dados=dados)

        if not EmpresasChaveService.chave_preenchida(chave):
            raise ValueError("Informe registro, empresa e filial para criar a empresa.")

        if EmpresasChaveService.existe(
            banco=banco,
            db_alias=db_alias,
            dados=chave,
        ):
            raise ValueError("Ja existe uma empresa com o registro, empresa e filial informados.")

        return Empresas.objects.using(db_alias).create(**dados)
