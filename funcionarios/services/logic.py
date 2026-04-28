from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from funcionarios.models import Funcionarios


class FuncionariosService:

    @staticmethod
    def listar_por_banco(*, banco: str, termo: str = None):
        qs = Funcionarios.objects.filter(registro=banco)
        if termo:
            qs = qs.filter(func_nome__icontains=termo)
        return qs.order_by("func_nome", "func_codi")

    @staticmethod
    def buscar(*, banco: str, func_codi: int):
        return Funcionarios.objects.filter(
            registro=banco, func_codi=func_codi
        ).first()

    @staticmethod
    def buscar_ou_404(*, banco: str, func_codi: int):
        return get_object_or_404(
            Funcionarios.objects, registro=banco, func_codi=func_codi
        )

    @staticmethod
    def salvar_form(*, banco: str, form) -> Funcionarios:
        instance = form.save(commit=False)
        instance.registro = banco
        instance.save()
        return instance

    @staticmethod
    def remover(*, banco: str, instance: Funcionarios) -> None:
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