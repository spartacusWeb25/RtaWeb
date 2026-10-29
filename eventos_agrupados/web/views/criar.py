from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from eventos_agrupados.mixin import EventosAgrupadosMixin
from eventos_agrupados.services.logic import EventosAgrupadosService
from eventos_agrupados.web.forms import EventosAgrupadosForm


class EventosAgrupadosCreateView(EventosAgrupadosMixin, SuccessMessageMixin, CreateView):
    model = None
    form_class = EventosAgrupadosForm
    template_name = "eventos_agrupados/form.html"
    success_message = "Configuração de eventos agrupados cadastrado com sucesso."

    def dispatch(self, request, *args, **kwargs):
        existente = EventosAgrupadosService.obter(
            banco=self.banco_limpo,
            even_empr=self.EMPRESA_FIXA_CODIGO,
            even_fili=self.FILIAL_FIXA_CODIGO,
            db_alias=self.db_alias,
        )
        if existente is not None:
            return redirect(reverse_lazy("eventos_agrupados:editar") + f"?banco={request.banco or 'rta0001'}")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial["registro"] = self.banco_limpo
        initial["even_empr"] = self.obter_codigo_empresa_contexto()
        initial["even_fili"] = self.obter_codigo_filial_contexto()
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["operacao"] = "criar"
        ctx["titulo"] = "Novo evento agrupado para cálculo"
        ctx["modo_edicao"] = False
        return ctx

    def form_valid(self, form):
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        try:
            EventosAgrupadosService.salvar_form(
                form,
                banco=self.banco_limpo,
                db_alias=self.db_alias,
                even_empr=empr,
                even_fili=fili,
                operacao="criar",
            )
        except Exception as exc:
            from django.core.exceptions import ValidationError

            if isinstance(exc, ValidationError):
                form.add_error(None, str(exc))
            else:
                form.add_error(None, str(exc))
            return self.form_invalid(form)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("eventos_agrupados:listar") + f"?banco={self.request.banco or 'rta0001'}"
