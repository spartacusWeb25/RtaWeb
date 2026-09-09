from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from eventos.services import EventosService
from eventos.mixin import EventoMixin
from eventos.utils import _has_errors


class EventoCreateView(EventoMixin, CreateView):
    def get_initial(self):
        initial = super().get_initial()
        if not initial.get("even_empr"):
            initial["even_empr"] = self.obter_codigo_empresa_contexto()
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Novo Evento"
        ctx["modo_edicao"] = False
        erros_por_aba = _has_errors(ctx["form"])
        ctx["has_errors"] = any(erros_por_aba.values())
        ctx["abas_com_erro"] = erros_por_aba
        return ctx

    def form_valid(self, form):
        try:
            even_empr = int(self.obter_codigo_empresa_contexto(form))
            EventosService.salvar_form(
                banco=self.request.banco,
                even_empr=even_empr,
                db_alias=self.request.db_alias,
                form=form,
            )
            messages.success(self.request, "Evento cadastrado com sucesso.")
            return redirect(reverse("eventos:listar") + f"?banco={self.request.banco}")
        except Exception as exc:
            messages.error(self.request, str(exc))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        return super().form_invalid(form)
