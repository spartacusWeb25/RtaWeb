from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from sindicatos.mixin import SindicatoTrabalhadoresMixin
from sindicatos.models import Sindicatos
from sindicatos.services.logic import SindicatoTrabalhadoresService, _digits_only


class SindicatoTrabalhadoresDeleteView(SindicatoTrabalhadoresMixin, TemplateView):
    template_name = "sindicatos/confirmar_exclusao.html"

    def get_queryset(self):
        return Sindicatos.objects.using(self.db_alias).filter(
            registro=self.banco_limpo
        )

    def get_object(self):
        obj = (
            self.get_queryset()
            .filter(
                sind_empr=self.kwargs["empr"],
                sind_fili=self.kwargs["fili"],
                sind_codi=self.kwargs["codi"],
            )
            .first()
        )
        if obj is None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["object"] = obj
        context["sindicato"] = obj
        return context

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        SindicatoTrabalhadoresService.excluir(obj, self.db_alias)
        messages.success(request, "Sindicato trabalhador excluído com sucesso.")
        return redirect(reverse("sindicatos:listar") + f"?banco={request.banco}")
