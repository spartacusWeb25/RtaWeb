from core.mixin import BancoObrigatorioMixin
from django.utils.safestring import mark_safe
import json
from terceiros.web.choices import CIDADES_POR_CODIGO
from sindicatospatronais.services.logic import (
    SindicatoPatronalService,
    proximo_codigo_sindicatopatronal,
    _digits_only,
)


class SindPatronalMixin(BancoObrigatorioMixin):

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
                valor = form.data.get("sind_empr")
                if valor not in (None, ""):
                    try:
                        return int(valor)
                    except Exception:
                        pass
            valor = form.initial.get("sind_empr")
            if valor not in (None, ""):
                try:
                    return int(valor)
                except Exception:
                    pass

        if hasattr(self, "object") and getattr(self, "object", None) is not None:
            return getattr(self.object, "sind_empr") or getattr(self.request, "empr_padrao_cod", None) or 1

        return getattr(self.request, "empr_padrao_cod", None) or 1

    def obter_codigo_filial_contexto(self, form=None):
        if form is not None:
            if form.is_bound:
                valor = form.data.get("sind_fili")
                if valor not in (None, ""):
                    try:
                        return int(valor)
                    except Exception:
                        pass
            valor = form.initial.get("sind_fili")
            if valor not in (None, ""):
                try:
                    return int(valor)
                except Exception:
                    pass

        if hasattr(self, "object") and getattr(self, "object", None) is not None:
            return getattr(self.object, "sind_fili") or getattr(self.request, "fili_padrao_cod", None) or 1

        return getattr(self.request, "fili_padrao_cod", None) or 1

    def obter_nome_empresa_contexto(self, form=None):
        codigo = self.obter_codigo_empresa_contexto(form=form)
        return SindicatoPatronalService.obter_nome_empresa(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=codigo,
        )

    def obter_nome_filial_contexto(self, form=None):
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        return SindicatoPatronalService.obter_nome_filial(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=empr,
            codigo_filial=fili,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["banco_limpo"] = self.banco_limpo
        ctx["cidades_por_codigo_json"] = mark_safe(
            json.dumps(CIDADES_POR_CODIGO, ensure_ascii=False)
        )
        if "form" in ctx:
            ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=ctx["form"])
            ctx["filial_nome"] = self.obter_nome_filial_contexto(form=ctx["form"])
        if not ctx.get("cidades_json"):
            try:
                from cidades.services.listar import ListarCidadesService
                cidades = ListarCidadesService.listar_todas_json(db_alias=self.db_alias)
                ctx["cidades_json"] = cidades
            except Exception:
                ctx["cidades_json"] = "[]"
        return ctx
