from licencas.models import Usuarios


class UsuariosService:
    @staticmethod
    def listar_por_registro(*, registro, termo=None):
        qs = Usuarios.objects.using("default").filter(registro=registro)
        if termo:
            qs = qs.filter(usua_nome__icontains=termo)
        return qs.order_by("usua_nome", "usua_login")

    @staticmethod
    def buscar(*, registro, user_id):
        return Usuarios.objects.using("default").filter(registro=registro, id=user_id).first()

    @staticmethod
    def salvar(*, instance):
        instance.save(using="default")
        return instance

    @staticmethod
    def remover(*, instance):
        instance.delete(using="default")
