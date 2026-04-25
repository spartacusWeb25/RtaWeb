from funcionarios.models import Funcionarios


class FuncionariosService:
    @staticmethod
    def listar_por_banco(*, banco, termo=None):
        qs = Funcionarios.objects.filter(registro=banco)
        if termo:
            qs = qs.filter(func_nome__icontains=termo)
        return qs.order_by("func_nome", "func_codi")

    @staticmethod
    def buscar(*, banco, func_codi):
        return Funcionarios.objects.filter(registro=banco, func_codi=func_codi).first()

    @staticmethod
    def salvar(*, instance):
        instance.save(using="default")
        return instance

    @staticmethod
    def remover(*, instance):
        instance.delete(using="default")
