from setores.models import Setoresrh


class ListarSetoresrhService:
    LIMITE_MAXIMO = 100

    @staticmethod
    def listar(*, banco, db_alias, empresa=None, referencia=None, descricao=None, codigo=None):
        qs = Setoresrh.objects.using(db_alias).filter(
            registro=banco
        )
        if descricao:
            qs = qs.filter(seto_desc__icontains=descricao)
        if referencia:
            qs = qs.filter(seto_refe__icontains=referencia)

        if empresa:
            qs = qs.filter(seto_empr__icontains=empresa)
        
        if codigo:
            qs = qs.filter(seto_codi__icontains=codigo)

        return qs.order_by("seto_codi")[:ListarSetoresrhService.LIMITE_MAXIMO]
