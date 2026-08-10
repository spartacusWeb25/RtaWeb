from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from empresas.models import Empresas
from funcionarios.models import Funcionarios


class FuncionariosService:

    @staticmethod
    def listar_por_banco(*, banco: str, termo: str = None):
        qs = Funcionarios.objects.filter(registro=banco)
        if termo:
            qs = qs.filter(func_nome__icontains=termo)
        return qs.order_by("func_nome", "func_codi")

    @staticmethod
    def buscar(*, banco: str, func_empr: int, func_fili: int, func_codi: int):
        return Funcionarios.objects.filter(
            registro=banco,
            func_empr=func_empr,
            func_fili=func_fili,
            func_codi=func_codi,
        ).first()

    @staticmethod
    def buscar_ou_404(*, banco: str, func_empr: int, func_fili: int, func_codi: int):
        return get_object_or_404(
            Funcionarios.objects,
            registro=banco,
            func_empr=func_empr,
            func_fili=func_fili,
            func_codi=func_codi,
        )

    @staticmethod
    def salvar_form(*, banco: str, db_alias: str = None, form) -> Funcionarios:
        instance = form.save(commit=False)
        instance.registro = banco
        if db_alias:
            instance.save(using=db_alias)
        else:
            instance.save()
        return instance

    @staticmethod
    def remover(*, banco: str, instance: Funcionarios) -> None:
        from dependentesrh.models import Dependentesrh
        db_alias = getattr(instance, '_state', None) and instance._state.db or None
        empr = getattr(instance, 'func_empr', None)
        fili = getattr(instance, 'func_fili', None)
        func = getattr(instance, 'func_codi', None)
        if banco and empr is not None and fili is not None and func is not None:
            try:
                qs_dep = Dependentesrh.objects
                if db_alias:
                    qs_dep = qs_dep.using(db_alias)
                qs_dep.filter(
                    registro=banco,
                    depe_empr=int(empr),
                    depe_fili=int(fili),
                    depe_func=int(func),
                ).delete()
            except Exception:
                pass
        instance.delete()

    @staticmethod
    def _validar_cpf_unico(*, banco: str, dados: dict, pk_atual=None) -> None:
        cpf = dados.get("func_cpf")
        if not cpf:
            return
        qs = Funcionarios.objects.filter(registro=banco, func_cpf=cpf)
        if pk_atual:
            qs = qs.exclude(func_codi=pk_atual)
        if qs.exists():
            raise ValidationError({"func_cpf": "Já existe um funcionário com este CPF."})

    @staticmethod
    def obter_nome_empresa(*, banco: str, db_alias: str = None, codigo_empresa=None) -> str:
        if not codigo_empresa:
            return ""

        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        empresa = (
            qs.filter(registro=banco, empr_empr=codigo_empresa)
            .order_by("empr_fili", "empr_nome")
            .first()
        )
        return getattr(empresa, "empr_nome", "") or ""

    @staticmethod
    def obter_empresa_padrao(*, banco: str, db_alias: str = None):
        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        return (
            qs.filter(registro=banco)
            .order_by("empr_empr", "empr_fili", "empr_nome")
            .first()
        )
