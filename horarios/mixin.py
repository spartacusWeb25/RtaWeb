from django.conf import settings


class HorariosMixin:
    db_alias_usar = "default"

    @property
    def db_alias(self):
        return self.db_alias_usar

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        banco = getattr(self.request, "banco", "")
        db_alias = getattr(self.request, "db_alias", self.db_alias_usar)
        kwargs["banco"] = banco
        kwargs["db_alias"] = db_alias
        return kwargs

    @staticmethod
    def _default(value, default):
        if value is None:
            return default
        if isinstance(value, str) and not value.strip():
            return default
        return value

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        banco = getattr(self.request, "banco", "")
        db_alias = getattr(self.request, "db_alias", self.db_alias_usar)

        from horarios.services.logic import HorariosService

        empr_codigo = 1
        fili_codigo = 1

        empr_nome = None
        filial_nome = None
        try:
            empr_nome = HorariosService.obter_nome_empresa(
                banco=banco,
                db_alias=db_alias,
                codigo_empresa=empr_codigo,
            )
        except Exception:
            empr_nome = None

        try:
            filial_nome = HorariosService.obter_nome_filial(
                banco=banco,
                db_alias=db_alias,
                codigo_empresa=empr_codigo,
                codigo_filial=fili_codigo,
            )
        except Exception:
            filial_nome = None

        empr_nome = self._default(empr_nome, "EMPRESA PADRÃO")
        filial_nome = self._default(filial_nome, empr_nome)

        ctx["empr_codigo"] = empr_codigo
        ctx["fili_codigo"] = fili_codigo
        ctx["empr_nome"] = empr_nome
        ctx["filial_nome"] = filial_nome

        try:
            ctx["proximo_codigo"] = HorariosService.proximo_codigo_quadro(
                banco=banco,
                db_alias=db_alias,
                empr_codigo=empr_codigo,
                fili_codigo=fili_codigo,
            )
        except Exception:
            ctx["proximo_codigo"] = 1

        object_instance = ctx.get("object")
        operacao = "criar"
        if object_instance is not None:
            try:
                tem_pk = all([
                    getattr(object_instance, "registro", None),
                    getattr(object_instance, "hora_empr", None) is not None,
                    getattr(object_instance, "hora_fili", None) is not None,
                    getattr(object_instance, "hora_codi", None) is not None,
                ])
                if tem_pk:
                    operacao = "editar"
            except Exception:
                pass
        ctx["operacao"] = operacao
        if ctx.get("object") is None:
            ctx["object"] = None
        return ctx
