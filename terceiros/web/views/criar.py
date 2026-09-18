from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from terceiros.mixin import TerceiroMixin
from terceiros.services.logic import TerceirosService, proximo_codigo_terceiro, _digits_only
from terceiros.utils import _has_errors


class TerceiroCreateView(TerceiroMixin, CreateView):
    success_url = reverse_lazy("terceiros:listar")

    def get_initial(self):
        initial = super().get_initial()
        empr = self.obter_codigo_empresa_contexto()
        fili = self.obter_codigo_filial_contexto()
        if not initial.get("terc_empr"):
            initial["terc_empr"] = empr
        if not initial.get("terc_fili"):
            initial["terc_fili"] = fili
        # --- Exibe o PROXIMO CODIGO automaticamente no input header
        #     (igual DepTerc: usuario ve o codigo novo antes mesmo de preencher)
        if (
            (not initial.get("terc_codi") or not str(initial.get("terc_codi") or "").isdigit())
            and getattr(self.request, "banco", None)
            and empr
            and fili
        ):
            try:
                initial["terc_codi"] = proximo_codigo_terceiro(
                    banco=_digits_only(self.request.banco),
                    db_alias=getattr(self, "db_alias", None) or "default",
                    empresa=int(empr),
                    filial=int(fili),
                )
            except Exception:
                initial["terc_codi"] = 1
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Novo Terceiro"
        ctx["modo_edicao"] = False
        ctx["has_errors"] = _has_errors(ctx["form"])
        ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=ctx["form"])
        ctx["filial_nome"] = self.obter_nome_filial_contexto(form=ctx["form"])

        # Novo terceiro: sem dependentes ainda
        ctx["dependentes_list"] = []
        ctx["dependentes_qtd"] = 0

        return ctx

    def form_valid(self, form):
        try:
            terc_empr = self.obter_codigo_empresa_contexto(form=form)
            terc_fili = self.obter_codigo_filial_contexto(form=form)
            TerceirosService.salvar_form(
                form=form,
                banco=self.request.banco,
                db_alias=self.db_alias,
                terc_empr=terc_empr,
                terc_fili=terc_fili,
                operacao="criar",
            )
            messages.success(self.request, "Terceiro cadastrado com sucesso.")
            return redirect(reverse("terceiros:listar") + f"?banco={self.request.banco}")
        except ValidationError as exc:
            form.add_error("terc_codi", "Ja existe um terceiro com este codigo e filial nesta licenca.")
            return self.form_invalid(form)
        except Exception as exc:
            messages.error(self.request, str(exc))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("terceiros:listar") + f"?banco={self.request.banco}"
