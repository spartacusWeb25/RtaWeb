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
