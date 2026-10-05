from core.mixin import BancoObrigatorioMixin
from prepara_recisoes.models import PreparaRescisoes
from prepara_recisoes.services.logic import PreparaRescisoesService
from prepara_recisoes.services.logic import _digits_only


class PreparaRescisoesMixin(BancoObrigatorioMixin):
    model = PreparaRescisoes
    template_name = "prepara_rescisoes/form.html"

    EMPRESA_FIXA_CODIGO = 1
    FILIAL_FIXA_CODIGO = 1

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        request.empr_padrao_cod = self.EMPRESA_FIXA_CODIGO
        request.fili_padrao_cod = self.FILIAL_FIXA_CODIGO
        return result

    @property
    def banco_limpo(self):
        return _digits_only(getattr(self.request, "banco", "") or "")

    @property
    def db_alias(self):
        return getattr(self.request, "db_alias", None) or "default"

    def get_queryset(self):
        return PreparaRescisoes.objects.using(self.db_alias).filter(
            registro=self.banco_limpo,
            prep_empr=self.EMPRESA_FIXA_CODIGO,
            prep_fili=self.FILIAL_FIXA_CODIGO,
        )

    def get_form_kwargs(self):
        from prepara_recisoes.web.forms import PreparaRescisoesForm
        self.form_class = PreparaRescisoesForm
        kwargs = super().get_form_kwargs()
        kwargs["db_alias"] = self.db_alias
        kwargs["banco"] = self.banco_limpo
        kwargs["empr_fixo"] = self.EMPRESA_FIXA_CODIGO
        kwargs["fili_fixo"] = self.FILIAL_FIXA_CODIGO
        return kwargs

    def get_object(self, queryset=None):
        from django.http import Http404
        qs = queryset or self.get_queryset()
        obj = qs.filter(
            registro=self.banco_limpo,
            prep_empr=self.EMPRESA_FIXA_CODIGO,
            prep_fili=self.FILIAL_FIXA_CODIGO,
            prep_codi=self.kwargs["prep_codi"],
        ).first()
        if obj is None:
            raise Http404
        return obj

    def obter_codigo_empresa_padrao(self):
        return self.EMPRESA_FIXA_CODIGO

    def obter_codigo_filial_padrao(self):
        return self.FILIAL_FIXA_CODIGO

    def obter_codigo_empresa_contexto(self, form=None):
        return self.EMPRESA_FIXA_CODIGO

    def obter_codigo_filial_contexto(self, form=None):
        return self.FILIAL_FIXA_CODIGO

    def obter_nome_empresa_contexto(self, form=None):
        return PreparaRescisoesService.obter_nome_empresa(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=self.EMPRESA_FIXA_CODIGO,
        )

    def obter_nome_filial_contexto(self, form=None):
        return PreparaRescisoesService.obter_nome_filial(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=self.EMPRESA_FIXA_CODIGO,
            codigo_filial=self.FILIAL_FIXA_CODIGO,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["banco_limpo"] = self.banco_limpo
        ctx["db_alias"] = self.db_alias
        ctx["empr_padrao_cod"] = self.EMPRESA_FIXA_CODIGO
        ctx["fili_padrao_cod"] = self.FILIAL_FIXA_CODIGO
        ctx["empr_padrao"] = self.EMPRESA_FIXA_CODIGO
        ctx["fili_padrao"] = self.FILIAL_FIXA_CODIGO
        if "form" in ctx:
            ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=ctx["form"])
            ctx["filial_nome"] = self.obter_nome_filial_contexto(form=ctx["form"])
        return ctx
