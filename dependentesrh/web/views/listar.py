from django.views.generic import ListView
from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from dependentesrh.models import Dependentesrh
from dependentesrh.services.listar import ListarDependentesrhService


def _buscar_funcionario_contexto(banco, db_alias, empresa, filial, funcionario):
    if not empresa or not filial or not funcionario:
        return None
    try:
        from funcionarios.models import Funcionarios

        return (
            Funcionarios.objects.using(db_alias)
            .filter(
                registro=banco,
                func_empr=int(empresa),
                func_fili=int(filial),
                func_codi=int(funcionario),
            )
            .values(
                "func_codi",
                "func_nome",
                "func_cargo",
                "func_empr",
                "func_fili",
                "func_admissao",
                "func_cpf",
            )
            .first()
        )
    except Exception:
        return None


class DependentesrhListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Dependentesrh
    context_object_name = "dependentesrh"
    template_name = "dependentesrh/listar.html"
    paginate_by = 20

    def get_queryset(self):
        empresa = self.request.GET.get("empresa")
        filial = self.request.GET.get("filial")
        funcionario = self.request.GET.get("funcionario")
        nome = self.request.GET.get("nome")
        cpf = self.request.GET.get("cpf")
        codigo = self.request.GET.get("codigo")
        invalido = self.request.GET.get("invalido")

        return ListarDependentesrhService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            empresa=empresa,
            filial=filial,
            funcionario=funcionario,
            nome=nome,
            cpf=cpf,
            codigo=codigo,
            invalido=invalido,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa = self.request.GET.get("empresa", "")
        filial = self.request.GET.get("filial", "")
        funcionario = self.request.GET.get("funcionario", "")
        context["empresa"] = empresa
        context["filial"] = filial
        context["funcionario"] = funcionario
        context["nome"] = self.request.GET.get("nome", "")
        context["cpf"] = self.request.GET.get("cpf", "")
        context["codigo"] = self.request.GET.get("codigo", "")
        context["invalido"] = self.request.GET.get("invalido", "")

        if empresa and filial and funcionario:
            context["funcionario_contexto"] = _buscar_funcionario_contexto(
                banco=self.request.banco,
                db_alias=self.request.db_alias,
                empresa=empresa,
                filial=filial,
                funcionario=funcionario,
            )
            try:
                from empresas.models import Empresas

                empresa_obj = (
                    Empresas.objects.using(self.request.db_alias)
                    .filter(registro=self.request.banco, empr_empr=int(empresa))
                    .values("empr_nome")
                    .first()
                )
                context["empresa_nome_contexto"] = (
                    empresa_obj["empr_nome"] if empresa_obj else ""
                )
            except Exception:
                context["empresa_nome_contexto"] = ""
        return context
