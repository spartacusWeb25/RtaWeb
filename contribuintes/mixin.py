from django.http import Http404
from core.mixin import BancoObrigatorioMixin
from contribuintes.models import Contribuintes
from contribuintes.services.logic import ContribuintesService
from contribuintes.web.forms import ContribuinteForm
from contribuintes.web.choices import COUNTRY_CHOICES, _TOP_CIDADES_IBGE
from django.utils.safestring import mark_safe
import json


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


class BancoObrigatorioMixin(BancoObrigatorioMixin):
    pass


class ContribuinteMixin(BancoObrigatorioMixin):
    model = Contribuintes
    form_class = ContribuinteForm
    template_name = "contribuintes/form.html"

    @property
    def banco_limpo(self) -> str:
        return _digits_only(self.request.banco)

    @property
    def db_alias(self) -> str:
        return self.request.db_alias

    def get_queryset(self):
        return Contribuintes.objects.using(self.db_alias).filter(
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
            contr_empr=self.kwargs["empr"],
            contr_fili=self.kwargs["fili"],
            contr_codi=self.kwargs["codi"],
        ).first()
        if obj is None:
            raise Http404
        return obj

    def obter_codigo_empresa_contexto(self, form=None):
        if form is not None:
            if form.is_bound:
                valor = form.data.get("contr_empr")
                if valor not in (None, ""):
                    return valor
            valor = form.initial.get("contr_empr")
            if valor not in (None, ""):
                return valor

        if hasattr(self, "object") and getattr(self, "object", None) is not None:
            return getattr(self.object, "contr_empr", "") or ""

        empresa_padrao = ContribuintesService.obter_empresa_padrao(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
        )
        return getattr(empresa_padrao, "empr_empr", "") or ""

    def obter_codigo_filial_contexto(self, form=None):
        if form is not None:
            if form.is_bound:
                valor = form.data.get("contr_fili")
                if valor not in (None, ""):
                    return valor
            valor = form.initial.get("contr_fili")
            if valor not in (None, ""):
                return valor

        if hasattr(self, "object") and getattr(self, "object", None) is not None:
            return getattr(self.object, "contr_fili", "") or ""

        filial_padrao = ContribuintesService.obter_filial_padrao(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
        )
        return getattr(filial_padrao, "empr_fili", "") or 1

    def obter_nome_empresa_contexto(self, form=None):
        codigo_empresa = self.obter_codigo_empresa_contexto(form=form)
        return ContribuintesService.obter_nome_empresa(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=codigo_empresa,
        )

    def obter_nome_filial_contexto(self, form=None):
        codigo_empresa = self.obter_codigo_empresa_contexto(form=form)
        codigo_filial = self.obter_codigo_filial_contexto(form=form)
        return ContribuintesService.obter_nome_filial(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=codigo_empresa,
            codigo_filial=codigo_filial,
        )

    def obter_paises_lista(self):
        result = []
        for valor, label in COUNTRY_CHOICES:
            if valor in (None, ""):
                continue
            try:
                cod_num = int(valor)
            except Exception:
                continue
            nome = label.split(" - ", 1)[1] if " - " in label else str(label)
            result.append({
                "codigo_num": cod_num,
                "nome": nome,
                "label": label,
            })
        return result

    def obter_cidades_lista(self):
        result = []
        for codigo, nome, uf in _TOP_CIDADES_IBGE:
            try:
                cod_num = int(codigo)
            except Exception:
                continue
            result.append({
                "codigo_num": cod_num,
                "nome": nome,
                "uf": uf,
                "label": f"{codigo:0>7} — {nome} / {uf}",
            })
        return result

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["empr_codigo"] = self.obter_codigo_empresa_contexto(form=ctx.get("form")) or 1
        ctx["fili_codigo"] = self.obter_codigo_filial_contexto(form=ctx.get("form")) or 1

        mapa_cargos_cbo = {}
        try:
            from cargos.services.logic import CargosService

            banco_clean = self.banco_limpo or ""
            empr_int = int(ctx.get("empr_codigo") or 1) or 1
            fili_int = int(ctx.get("fili_codigo") or 1) or 1
            listagem = CargosService.listar_cargos(
                banco=banco_clean,
                db_alias=self.db_alias,
                codigo_empresa=empr_int,
                codigo_filial=fili_int,
                incluir_inativos=True,
            )
            for item in listagem or []:
                try:
                    chave = int(item.get("codi"))
                except Exception:
                    continue
                entrada = {
                    "cbo": item.get("cbo_codi") or "",
                    "desc": item.get("cbo_desc") or "",
                    "cargo_nome": item.get("label") or "",
                }
                mapa_cargos_cbo[chave] = entrada
        except Exception:
            mapa_cargos_cbo = {}
        ctx["mapa_cargos_cbo"] = mapa_cargos_cbo
        try:
            ctx["mapa_cargos_cbo_json"] = json.dumps(mapa_cargos_cbo, ensure_ascii=False)
        except Exception:
            ctx["mapa_cargos_cbo_json"] = "{}"
        return ctx
