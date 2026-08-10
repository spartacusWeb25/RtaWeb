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
