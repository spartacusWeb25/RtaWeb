from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import FormView

from calendario.models import Calendariorh
from calendario.services import CalendarioService
from calendario.web.forms import CalendarioEventoForm
from core.mixin import BancoObrigatorioMixin


class CalendarioEventoCreateView(BancoObrigatorioMixin, FormView):
    form_class = CalendarioEventoForm

    def form_valid(self, form):
        evento = Calendariorh(
            registro=self._gerar_registro(),
            cale_cida=form.cleaned_data["cale_cida"],
            cale_refe=form.cleaned_data["cale_refe"],
            cale_data=form.cleaned_data["cale_data"],
            cale_dia_desc=form.cleaned_data["cale_dia_desc"],
            _log_data=timezone.localdate(),
            _log_time=timezone.localtime().time(),
        )
        CalendarioService.salvar(instance=evento, db_alias=self.request.db_alias)
        messages.success(self.request, "Evento de calendário cadastrado com sucesso.")
        return redirect(f"{reverse('home')}?banco={self.request.banco}")

    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível cadastrar o evento. Verifique os dados e tente novamente.")
        return redirect(f"{reverse('home')}?banco={self.request.banco}")

    @staticmethod
    def _gerar_registro() -> str:
        return timezone.now().strftime("%y%m%d%H%M%S%f")[:14]
