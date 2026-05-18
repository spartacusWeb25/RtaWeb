from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.db import IntegrityError
from core.exceptions import RegistroDuplicadoError
from core.mixin import BancoObrigatorioMixin
from folhamensal.models import Folhamensal
from folhamensal.services import FolhaMensalSalvarService
from folhamensal.web.forms import FolhaMensalForm


class FolhaMensalCreateView(BancoObrigatorioMixin, CreateView):
    model = Folhamensal
    form_class = FolhaMensalForm
    template_name = "folha/folha_mensal_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["banco"] = self.request.banco
        kwargs["db_alias"] = self.request.db_alias
        return kwargs
    
    def form_invalid(self, form):
        print("FORM INVALID:", form.errors)
        print("BANCO:", self.request.banco)
        print("DB_ALIAS:", self.request.db_alias)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("folha:folha_mensal_list")
    
    def form_valid(self, form):
        try:
            self.object = FolhaMensalSalvarService.criar(
                banco=self.request.banco,
                db_alias=self.request.db_alias,
                dados=form.cleaned_data,
            )

            messages.success(self.request, "Lançamento criado com sucesso.")
            return redirect(self.get_success_url())

        except IntegrityError as error:
            error = RegistroDuplicadoError.tratar_integrity_error(error)
            form.add_error(None, getattr(error, "message", str(error)))
            return self.form_invalid(form)