from core.mixin import BancoObrigatorioMixin
from django.utils.safestring import mark_safe
import json

from cargos.services.logic import (
    CargosService,
    proximo_codigo_cargo,
    _digits_only,
)


class CargosMixin(BancoObrigatorioMixin):

    @property
    def banco_limpo(self):
        return _digits_only(getattr(self.request, "banco", "") or "")

    @property
    def db_alias(self):
        return getattr(self.request, "db_alias", None) or "default"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["db_alias"] = self.db_alias
        kwargs["banco"] = self.banco_limpo
        return kwargs

    def obter_codigo_empresa_contexto(self, form=None):
        if form is not None:
            if form.is_bound:
                valor = form.data.get("carg_empr")
                if valor not in (None, ""):
                    try:
                        return int(valor)
                    except Exception:
                        pass
            valor = form.initial.get("carg_empr")
            if valor not in (None, ""):
                try:
                    return int(valor)
                except Exception:
                    pass

        if hasattr(self, "object") and getattr(self, "object", None) is not None:
            return getattr(self.object, "carg_empr") or getattr(self.request, "empr_padrao_cod", None) or 1

        return getattr(self.request, "empr_padrao_cod", None) or 1

    def obter_codigo_filial_contexto(self, form=None):
        if form is not None:
            if form.is_bound:
                valor = form.data.get("carg_fili")
                if valor not in (None, ""):
                    try:
                        return int(valor)
                    except Exception:
                        pass
            valor = form.initial.get("carg_fili")
            if valor not in (None, ""):
                try:
                    return int(valor)
                except Exception:
                    pass

        if hasattr(self, "object") and getattr(self, "object", None) is not None:
            return getattr(self.object, "carg_fili") or getattr(self.request, "fili_padrao_cod", None) or 1

        return getattr(self.request, "fili_padrao_cod", None) or 1

    def obter_nome_empresa_contexto(self, form=None):
        codigo = self.obter_codigo_empresa_contexto(form=form)
        return CargosService.obter_nome_empresa(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=codigo,
        )

    def obter_nome_filial_contexto(self, form=None):
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        return CargosService.obter_nome_filial(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=empr,
            codigo_filial=fili,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["banco_limpo"] = self.banco_limpo
        if "form" in ctx:
            ctx["empr_codigo"] = self.obter_codigo_empresa_contexto(form=ctx["form"])
            ctx["fili_codigo"] = self.obter_codigo_filial_contexto(form=ctx["form"])
            ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=ctx["form"])
            ctx["filial_nome"] = self.obter_nome_filial_contexto(form=ctx["form"])
        else:
            ctx["empr_codigo"] = self.obter_codigo_empresa_contexto()
            ctx["fili_codigo"] = self.obter_codigo_filial_contexto()
        try:
            cbos = CargosService.listar_cbos(banco=self.banco_limpo, db_alias=self.db_alias)
        except Exception:
            cbos = []
        ctx["cbos_disponiveis_json"] = mark_safe(json.dumps(cbos, ensure_ascii=False))
        return ctx
