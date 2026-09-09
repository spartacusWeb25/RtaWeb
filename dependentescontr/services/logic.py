from dependentescontr.services.criar import DependentescontrCriarService
from dependentescontr.services.editar import DependentescontrEditarService
from dependentescontr.services.excluir import DependentescontrExcluirService


class DependentescontrService:

    @staticmethod
    def salvar_form(form, banco, db_alias, depecontr_empr=None, depecontr_fili=None, depecontr_contr=None, **kwargs):
        from dependentescontr.services.chave import DependentescontrChaveService

        dados = form.cleaned_data.copy()
        dados["registro"] = banco

        if depecontr_empr is not None:
            dados["depecontr_empr"] = depecontr_empr
        if depecontr_fili is not None:
            dados["depecontr_fili"] = depecontr_fili
        if depecontr_contr is not None:
            dados["depecontr_contr"] = depecontr_contr

        if not dados.get("depecontr_codi") and dados.get("depecontr_contr"):
            dados["depecontr_codi"] = DependentescontrChaveService.proximo_codigo(
                banco=banco,
                db_alias=db_alias,
                empresa=dados.get("depecontr_empr"),
                filial=dados.get("depecontr_fili"),
                contribuinte=dados.get("depecontr_contr"),
            )

        existe = DependentescontrChaveService.existe(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if existe:
            return DependentescontrEditarService.editar(
                banco=banco,
                db_alias=db_alias,
                dados=dados,
            )
        else:
            return DependentescontrCriarService.criar(
                banco=banco,
                db_alias=db_alias,
                dados=dados,
            )

    @staticmethod
    def excluir_dependentecontr(banco, db_alias, dados):
        return DependentescontrExcluirService.excluir(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

    @staticmethod
    def obter_empresa_padrao(banco, db_alias):
        try:
            from contribuintes.services.logic import ContribuintesService
            return ContribuintesService.obter_empresa_padrao(banco=banco, db_alias=db_alias)
        except Exception:
            return None

    @staticmethod
    def obter_filial_padrao(banco, db_alias):
        try:
            from contribuintes.services.logic import ContribuintesService
            return ContribuintesService.obter_filial_padrao(banco=banco, db_alias=db_alias)
        except Exception:
            return None

    @staticmethod
    def proximo_codigo(*, banco, db_alias, empresa, filial, contribuinte):
        from dependentescontr.services.chave import DependentescontrChaveService
        return DependentescontrChaveService.proximo_codigo(
            banco=banco,
            db_alias=db_alias,
            empresa=empresa,
            filial=filial,
            contribuinte=contribuinte,
        )
