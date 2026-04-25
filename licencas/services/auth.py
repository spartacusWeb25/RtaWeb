from licencas.models import LicencasRta, Logado, Usuarios


class LoginRtaService:
    @staticmethod
    def autenticar(*, registro, usuario, senha, ip):
        licenca = LicencasRta.objects.using("licencas").filter(
            lice_docu=registro,
        ).first()

        if not licenca:
            return False, "Não autorizado", None

        if licenca.lice_bloq:
            return False, "Licença bloqueada", None

        user = Usuarios.objects.using("default").filter(
            registro=registro,
            usua_login=usuario,
            usua_senh=senha,
            usua_ativ=True,
        ).first()

        if not user:
            return False, "Usuário ou senha incorreta ou usuário não está ativo!", None

        Logado.objects.using("default").filter(
            registro=registro,
            usuario=user.id,
            ativo=True,
        ).update(
            ativo=False,
            obs="Encerrado por entrar em outra sessão",
            ip=ip,
        )

        Logado.objects.using("default").create(
            registro=registro,
            usuario=user.id,
            ativo=True,
            ip=ip,
        )
        return True, "Login realizado com sucesso", {
            "banco": registro,
            "licenca_nome": licenca.lice_banc,
            "usuario_id": user.id,
            "usuario_nome": user.usua_login,
            "usuario_grupo": user.usua_grup,
            "usuario_super": user.super,

        }
