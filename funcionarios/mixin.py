from django.http import Http404
from core.mixin import BancoObrigatorioMixin
from funcionarios.models import Funcionarios
from funcionarios.services import FuncionariosService
from funcionarios.web.forms import FuncionarioForm


class FuncionarioMixin(BancoObrigatorioMixin):
    model = Funcionarios
    form_class = FuncionarioForm
    template_name = "funcionarios/funcionario_form.html"

    @property
    def db_alias(self) -> str:
        return self.request.db_alias

    def get_queryset(self):
        return Funcionarios.objects.using(self.db_alias).filter(
            registro=self.request.banco
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["db_alias"] = self.db_alias
        banco = getattr(self.request, "banco", "") or ""
        kwargs["banco"] = banco

        empr_default = self.obter_codigo_empresa_contexto()
        fili_default = self.obter_filial_empresa_contexto()
        try:
            empr_int = int(empr_default) if str(empr_default or "").isdigit() else 1
        except Exception:
            empr_int = 1
        try:
            fili_int = int(fili_default) if str(fili_default or "").isdigit() else 1
        except Exception:
            fili_int = 1
        kwargs["empr_codigo"] = empr_int
        kwargs["fili_codigo"] = fili_int
        return kwargs

    def get_object(self, queryset=None):
        qs = queryset or self.get_queryset()
        obj = qs.filter(
            registro=self.request.banco,
            func_empr=self.kwargs["func_empr"],
            func_codi=self.kwargs["func_codi"],
            func_fili=self.kwargs["func_fili"],
        ).first()
        if obj is None:
            raise Http404
        return obj

    def obter_codigo_empresa_contexto(self, form=None):
        if form is not None:
            if form.is_bound:
                valor = form.data.get("func_empr")
                if valor not in (None, ""):
                    return valor
            valor = form.initial.get("func_empr")
            if valor not in (None, ""):
                return valor

        if hasattr(self, "object") and getattr(self, "object", None) is not None:
            return getattr(self.object, "func_empr", "") or ""

        empresa_padrao = FuncionariosService.obter_empresa_padrao(
            banco=self.request.banco,
            db_alias=self.db_alias,
        )
        return getattr(empresa_padrao, "empr_empr", "") or ""

    def obter_filial_empresa_contexto(self, form=None):
        if form is not None:
            if form.is_bound:
                valor = form.data.get("func_fili")
                if valor not in (None, ""):
                    return valor
            valor = form.initial.get("func_fili")
            if valor not in (None, ""):
                return valor

        if hasattr(self, "object") and getattr(self, "object", None) is not None:
            return getattr(self.object, "func_fili", "") or ""

        empresa_padrao = FuncionariosService.obter_empresa_padrao(
            banco=self.request.banco,
            db_alias=self.db_alias,
        )
        return getattr(empresa_padrao, "empr_fili", "") or ""

    def obter_nome_empresa_contexto(self, form=None):
        codigo_empresa = self.obter_codigo_empresa_contexto(form=form)
        return FuncionariosService.obter_nome_empresa(
            banco=self.request.banco,
            db_alias=self.db_alias,
            codigo_empresa=codigo_empresa,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        banco = getattr(self.request, "banco", "") or ""
        empr = self.obter_codigo_empresa_contexto(form=ctx.get("form"))
        fili = self.obter_filial_empresa_contexto(form=ctx.get("form"))
        try:
            empr_int = int(empr) if str(empr or "").isdigit() else 1
        except Exception:
            empr_int = 1
        try:
            fili_int = int(fili) if str(fili or "").isdigit() else 1
        except Exception:
            fili_int = 1

        mapa_cargos_cbo = {}
        mapa_funcoes_cbo = {}
        try:
            from cargos.services.logic import CargosService
            lista_cargos = CargosService.listar_cargos(
                banco=banco,
                db_alias=self.db_alias,
                codigo_empresa=empr_int,
                codigo_filial=fili_int,
                incluir_inativos=True,
            )
            for item in lista_cargos:
                chave = int(item["codi"])
                entrada = {"cbo": item.get("cbo_codi") or "", "desc": item.get("cbo_desc") or "",
                           "cargo_nome": item.get("label") or ""}
                mapa_cargos_cbo[chave] = entrada
                mapa_funcoes_cbo[chave] = entrada
        except Exception:
            mapa_cargos_cbo = {}
            mapa_funcoes_cbo = {}
        ctx["mapa_cargos_cbo"] = mapa_cargos_cbo
        ctx["mapa_funcoes_cbo"] = mapa_funcoes_cbo
        try:
            import json
            ctx["mapa_cargos_cbo_json"] = json.dumps(mapa_cargos_cbo, ensure_ascii=False)
            ctx["mapa_funcoes_cbo_json"] = json.dumps(mapa_funcoes_cbo, ensure_ascii=False)
        except Exception:
            ctx["mapa_cargos_cbo_json"] = "{}"
            ctx["mapa_funcoes_cbo_json"] = "{}"
        return ctx
