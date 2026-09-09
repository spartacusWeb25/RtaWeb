from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.mixin import BancoObrigatorioMixin
from eventos.models import Eventos
from eventos.services import EventosService


class EventoDeleteView(BancoObrigatorioMixin, TemplateView):
    template_name = "eventos/confirmar_exclusao.html"

    def get_evento(self):
        evento = (
            self.get_queryset()
            .filter(
                registro=self.request.banco,
                even_empr=self.kwargs["even_empr"],
                even_codi=self.kwargs["even_codi"],
            )
            .first()
        )
        if evento is None:
            raise Http404
        return evento

    def get_queryset(self):
        return Eventos.objects.using(self.request.db_alias).filter(
            registro=self.request.banco
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["evento"] = self.get_evento()
        return context

    def post(self, request, *args, **kwargs):
        evento = self.get_evento()
        EventosService.remover(
            banco=request.banco,
            instance=evento,
        )
        messages.success(request, "Evento removido com sucesso.")
        return redirect(reverse("eventos:listar") + f"?banco={request.banco}")
