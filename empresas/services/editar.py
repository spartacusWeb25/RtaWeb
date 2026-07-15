from empresas.services.chave import EmpresasChaveService
from empresas.models import Empresas


class EmpresasEditarService:

    @staticmethod
    def editar(*, banco, db_alias, dados):
        dados = dict(dados)
        chave_original = {
            "registro": dados.pop("_original_registro", None) or dados.get("registro"),
            "empr_empr": dados.pop("_original_empr_empr", None) or dados.get("empr_empr"),
            "empr_fili": dados.pop("_original_empr_fili", None) or dados.get("empr_fili"),
        }

        if not EmpresasChaveService.chave_preenchida(chave_original):
            raise ValueError("Informe o código para localizar a empresa.")

        empresa = EmpresasChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=chave_original,
        )

        if not empresa:
            raise ValueError("Empresa não encontrada.")

        nova_chave = EmpresasChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not EmpresasChaveService.chave_preenchida(nova_chave):
            raise ValueError("Informe o código para salvar a empresa.")

        if nova_chave != chave_original and EmpresasChaveService.existe(
            banco=banco,
            db_alias=db_alias,
            dados=nova_chave,
        ):
            raise ValueError("Já existe uma empresa com o código e filial informados.")

        valores_atualizados = {
            campo: valor
            for campo, valor in dados.items()
            if not campo.startswith("_original_")
        }

        if not valores_atualizados:
            return empresa

        Empresas.objects.using(db_alias).filter(**chave_original).update(**valores_atualizados)

        return Empresas.objects.using(db_alias).filter(**nova_chave).first()
