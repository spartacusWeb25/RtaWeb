from licencas.models import Usuarios


class UsuariosService:
    @staticmethod
    def listar_por_registro(*, registro, db_alias, termo=None, ordenar=None):
        qs = Usuarios.objects.using(db_alias).filter(registro=registro)
        if termo:
            qs = qs.filter(usua_nome__icontains=termo)

        if ordenar == "nome_desc":
            return qs.order_by("-usua_nome", "-usua_login")

        return qs.order_by("usua_nome", "usua_login")

    @staticmethod
    def buscar(*, registro, user_id, db_alias):
        return Usuarios.objects.using(db_alias).filter(registro=registro, id=user_id).first()

    @staticmethod
    def proximo_id(*, db_alias):
        ultimo_id = (
            Usuarios.objects.using(db_alias)
            .order_by("-id")
            .values_list("id", flat=True)
            .first()
        ) or 0
        return ultimo_id + 1

    @staticmethod
    def salvar(*, instance, db_alias):
        if instance.id is None:
            instance.id = UsuariosService.proximo_id(db_alias=db_alias)
        instance.save(using=db_alias)
        return instance

    @staticmethod
    def remover(*, instance, db_alias):
        instance.delete(using=db_alias)
