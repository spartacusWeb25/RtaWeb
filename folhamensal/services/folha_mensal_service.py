from folhamensal.models import Folhamensal


class FolhaMensalService:
    @staticmethod
    def listar(*, banco, referencia=None, empresa=None, filial=None, funcionario=None):
        if not hasattr(Folhamensal.objects, "do_banco"):
            raise AttributeError("O método 'do_banco' não foi encontrado na queryset do modelo Folhamensal.")

        qs = Folhamensal.objects.do_banco(banco)

        if referencia:
            qs = qs.filter(fome_refe=referencia)

        if empresa:
            qs = qs.filter(fome_empr=empresa)

        if filial:
            qs = qs.filter(fome_fili=filial)

        if funcionario:
            qs = qs.filter(fome_func=funcionario)
        print("SQL:", qs.query)
        print("TOTAL:", qs.count())

        return qs.order_by("fome_func", "fome_even")