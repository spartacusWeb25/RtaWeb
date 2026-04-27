from folhamensal.models import Folhamensal


class FolhaMensalService:
    @staticmethod
    def listar(*, banco, referencia=None, empresa=None, filial=None, funcionario=None):
        qs = Folhamensal.objects.do_banco(banco)

        if referencia:
            qs = qs.filter(fome_refe=referencia)
        if empresa:
            qs = qs.filter(fome_empr=empresa)
        if filial:
            qs = qs.filter(fome_fili=filial)
        if funcionario:
            qs = qs.filter(fome_func=funcionario)

        return qs.order_by("fome_func", "fome_even")

    @staticmethod
    def buscar(*, banco, fome_func, fome_refe, fome_even):
        return Folhamensal.objects.filter(
            registro=banco,
            fome_func=fome_func,
            fome_refe=fome_refe,
            fome_even=fome_even,
        ).first()

    @staticmethod
    def salvar(*, instance):
        instance.save(using="default")
        return instance

    @staticmethod
    def remover(*, instance):
        instance.delete(using="default")
        
  