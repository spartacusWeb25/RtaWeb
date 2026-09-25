from django.http import Http404
from django.utils.safestring import mark_safe
from core.mixin import BancoObrigatorioMixin
from terceiros.models import Terceiros
from terceiros.services.logic import TerceirosService
from terceiros.web.choices import CIDADES_POR_CODIGO
from terceiros.web.forms import TerceirosForm
import json


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


class BancoObrigatorioMixin(BancoObrigatorioMixin):
    pass


class TerceiroMixin(BancoObrigatorioMixin):
    model = Terceiros
    form_class = TerceirosForm
    template_name = "terceiros/form.html"

    @property
    def banco_limpo(self) -> str:
        return _digits_only(self.request.banco)

    @property
    def db_alias(self) -> str:
        return self.request.db_alias

    def get_queryset(self):
        return Terceiros.objects.using(self.db_alias).filter(
            registro=self.banco_limpo
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["db_alias"] = self.db_alias
        kwargs["banco"] = self.banco_limpo
        kwargs["empr_codigo"] = self.obter_codigo_empresa_contexto() or 1
        kwargs["fili_codigo"] = self.obter_codigo_filial_contexto() or 1
        return kwargs

    def get_object(self, queryset=None):
        qs = queryset or self.get_queryset()
        obj = qs.filter(
            registro=self.banco_limpo,
            terc_empr=self.kwargs["empr"],
            terc_fili=self.kwargs["fili"],
            terc_codi=self.kwargs["codi"],
        ).first()
        if obj is None:
            raise Http404
        return obj

    def obter_codigo_empresa_contexto(self, form=None):
        if form is not None:
            if form.is_bound:
                valor = form.data.get("terc_empr")
                if valor not in (None, ""):
                    return valor
            valor = form.initial.get("terc_empr")
            if valor not in (None, ""):
                return valor

        if hasattr(self, "object") and getattr(self, "object", None) is not None:
            return getattr(self.object, "terc_empr", "") or ""

        empresa_padrao = TerceirosService.obter_empresa_padrao(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
        )
        return getattr(empresa_padrao, "empr_empr", "") or ""

    def obter_codigo_filial_contexto(self, form=None):
        if form is not None:
            if form.is_bound:
                valor = form.data.get("terc_fili")
                if valor not in (None, ""):
                    return valor
            valor = form.initial.get("terc_fili")
            if valor not in (None, ""):
                return valor

        if hasattr(self, "object") and getattr(self, "object", None) is not None:
            return getattr(self.object, "terc_fili", "") or ""

        filial_padrao = TerceirosService.obter_filial_padrao(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
        )
        return getattr(filial_padrao, "empr_fili", "") or 1

    def obter_nome_empresa_contexto(self, form=None):
        codigo_empresa = self.obter_codigo_empresa_contexto(form=form)
        return TerceirosService.obter_nome_empresa(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=codigo_empresa,
        )

    def obter_nome_filial_contexto(self, form=None):
        codigo_empresa = self.obter_codigo_empresa_contexto(form=form)
        codigo_filial = self.obter_codigo_filial_contexto(form=form)
        return TerceirosService.obter_nome_filial(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=codigo_empresa,
            codigo_filial=codigo_filial,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["cidades_por_codigo_json"] = mark_safe(
            json.dumps(CIDADES_POR_CODIGO, ensure_ascii=False)
        )
        ctx["banco_limpo"] = self.banco_limpo
        ctx["empr_codigo"] = self.obter_codigo_empresa_contexto(form=ctx.get("form")) or 1
        ctx["fili_codigo"] = self.obter_codigo_filial_contexto(form=ctx.get("form")) or 1
        return ctx
