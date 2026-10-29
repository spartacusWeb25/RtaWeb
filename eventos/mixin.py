from django.http import Http404
from core.mixin import BancoObrigatorioMixin
from eventos.models import Eventos
from eventos.services import EventosService
from eventos.web.forms import EventoForm


class EventoMixin(BancoObrigatorioMixin):
    model = Eventos
    form_class = EventoForm
    template_name = "eventos/form.html"

    @property
    def db_alias(self) -> str:
        return self.request.db_alias

    def get_queryset(self):
        return Eventos.objects.using(self.db_alias).filter(
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
            even_empr=self.kwargs["even_empr"],
            even_codi=self.kwargs["even_codi"],
        ).first()
        if obj is None:
            raise Http404
        return obj

    def obter_codigo_empresa_contexto(self, form=None):
        if form is not None:
            if form.is_bound:
                valor = form.data.get("even_empr")
                if valor not in (None, ""):
                    return valor
            valor = form.initial.get("even_empr")
            if valor not in (None, ""):
                return valor

        if hasattr(self, "object") and getattr(self, "object", None) is not None:
            return getattr(self.object, "even_empr", "") or ""

        empresa_padrao = EventosService.obter_empresa_padrao(
            banco=self.request.banco,
            db_alias=self.db_alias,
        )
        return getattr(empresa_padrao, "empr_empr", "") or ""

    def obter_codigo_filial_contexto(self):
        codigo_empresa = self.obter_codigo_empresa_contexto()
        filial_padrao = EventosService.obter_filial_padrao(
            banco=self.request.banco,
            db_alias=self.db_alias,
            codigo_empresa=codigo_empresa,
        )
        return getattr(filial_padrao, "empr_fili", "") or ""

    def obter_nome_empresa_contexto(self, form=None):
        codigo_empresa = self.obter_codigo_empresa_contexto(form=form)
        return EventosService.obter_nome_empresa(
            banco=self.request.banco,
            db_alias=self.db_alias,
            codigo_empresa=codigo_empresa,
        )

    def obter_nome_filial_contexto(self):
        codigo_empresa = self.obter_codigo_empresa_contexto()
        codigo_filial = self.obter_codigo_filial_contexto()
        return EventosService.obter_nome_filial(
            banco=self.request.banco,
            db_alias=self.db_alias,
            codigo_empresa=codigo_empresa,
            codigo_filial=codigo_filial,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx.get("form")
        ctx["empr_codigo"] = self.obter_codigo_empresa_contexto(form=form)
        ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=form)
        ctx["fili_codigo"] = self.obter_codigo_filial_contexto()
        ctx["filial_nome"] = self.obter_nome_filial_contexto()
        return ctx
