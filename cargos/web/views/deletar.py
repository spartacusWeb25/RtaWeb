from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404, redirect

from cargos.mixin import CargosMixin
from cargos.models import Cargos
from cargos.services.logic import CargosService, _digits_only


class CargoDeleteView(CargosMixin, DeleteView):
    model = Cargos
    template_name = "cargos/confirmar_exclusao.html"
    success_url_name = "cargos:listar"
    success_message = "Cargo excluído com sucesso."

    def get_object(self, queryset=None):
        empr = int(self.kwargs.get("empr") or 0)
        fili = int(self.kwargs.get("fili") or 0)
        codi = int(self.kwargs.get("codi") or 0)
        banco_limpo = _digits_only(self.request.banco or "")
        qs = Cargos.objects.using(self.db_alias).filter(
            registro=banco_limpo,
            carg_empr=empr,
            carg_fili=fili,
            carg_codi=codi,
        )
        return get_object_or_404(qs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["item_descricao"] = getattr(self.object, "carg_descricao", None) or f"Cargo #{getattr(self.object, 'carg_codi', '')}"
        return ctx

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            CargosService.excluir(self.object, db_alias=self.db_alias)
        except Exception as exc:
            messages.error(request, f"Não foi possível excluir: {exc}")
            return redirect(self.get_success_url())
        messages.success(request, self.success_message)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(self.success_url_name) + f"?banco={self.request.banco or 'rta0001'}"
