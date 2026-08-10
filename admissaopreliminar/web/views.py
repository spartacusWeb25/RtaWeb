from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from core.mixin import BancoObrigatorioMixin
from admissaopreliminar.services import AdmissaoPreliminarService
from admissaopreliminar.web.forms import AdmissaoPreliminarForm


class AdmissaoPreliminarView(BancoObrigatorioMixin, FormView):
    template_name = "admissaopreliminar/form.html"
    form_class = AdmissaoPreliminarForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        empresa_codigo = (
            self.request.POST.get("empresa")
            or self.request.GET.get("empresa")
            or self.get_initial().get("empresa")
        )
        empresa_nome = AdmissaoPreliminarService.obter_nome_empresa(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            codigo_empresa=empresa_codigo,
        )
        kwargs["empresa_nome"] = empresa_nome
        kwargs["banco"] = self.request.banco
        kwargs["db_alias"] = self.request.db_alias
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        if "empresa" in self.request.GET:
            initial["empresa"] = self.request.GET.get("empresa")
        elif not initial.get("empresa"):
            inicial = AdmissaoPreliminarService.obter_codigo_empresa_inicial(
                banco=self.request.banco,
                db_alias=self.request.db_alias,
            )
            if inicial is not None:
                initial["empresa"] = inicial
        if "admissao" not in initial:
            from datetime import date

            initial["admissao"] = date.today()
        return initial

    def form_valid(self, form):
        AdmissaoPreliminarService.salvar_prefill_na_sessao(
            session=self.request.session,
            dados=form.cleaned_data,
        )
        messages.success(
            self.request,
            "Dados enviados para o cadastro de funcionarios. Complete os campos restantes e salve o registro.",
        )
        return redirect(f"{reverse('funcionarios:criar')}?banco={self.request.banco}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Admissao preliminar"
        return context
