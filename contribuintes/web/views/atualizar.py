from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView
from contribuintes.mixin import ContribuinteMixin
from contribuintes.services.logic import ContribuintesService
from contribuintes.utils import _has_errors
from dependentescontr.choices import TIPO_DEPENDENTE_CHOICES, TIPO_DEPENDENCIA_CHOICES


def _label_from_choices(value, choices):
    if value is None:
        return ""
    d = {k: v for k, v in choices}
    return d.get(value, str(value))


class ContribuinteUpdateView(ContribuinteMixin, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Editar Contribuinte"
        ctx["modo_edicao"] = True
        ctx["has_errors"] = _has_errors(ctx["form"])
        ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=ctx["form"])
        ctx["filial_nome"] = self.obter_nome_filial_contexto(form=ctx["form"])
        ctx["integracao_esocial_ok"] = bool(getattr(self.object, "contr_esocial_integrado", False))
        lista = []
        obj = ctx.get("object")
        if obj and getattr(obj, "contr_codi", None) and getattr(obj, "contr_empr", None) and getattr(obj, "contr_fili", None):
            try:
                from dependentescontr.models import Dependentescontr
                filtros = dict(
                    depecontr_empr=obj.contr_empr,
                    depecontr_fili=obj.contr_fili,
                    depecontr_contr=obj.contr_codi,
                )
                if self.request.banco:
                    filtros["registro"] = self.request.banco
                qs = Dependentescontr.objects.using(self.db_alias).filter(**filtros).order_by("depecontr_codi")
                for dep in qs:
                    dep.tipo_dependente_label = _label_from_choices(getattr(dep, "depecontr_tipo_dependente", None), TIPO_DEPENDENTE_CHOICES)
                    dep.tipo_dependencia_label = _label_from_choices(getattr(dep, "depecontr_tipo_dependencia", None), TIPO_DEPENDENCIA_CHOICES)
                    lista.append(dep)
                ctx["dependentescontr_qtd"] = len(lista)
                ctx["dependentescontr_url_criar"] = (
                    reverse("dependentescontr:criar")
                    + f"?banco={self.request.banco}&empr={int(obj.contr_empr)}&fili={int(obj.contr_fili)}&contr={int(obj.contr_codi)}"
                )
            except Exception:
                lista = []
                ctx["dependentescontr_qtd"] = 0
                ctx["dependentescontr_url_criar"] = ""
        else:
            ctx["dependentescontr_qtd"] = 0
            ctx["dependentescontr_url_criar"] = ""
        ctx["dependentescontr_list"] = lista
        ctx["paises_lista"] = self.obter_paises_lista()
        ctx["cidades_lista"] = self.obter_cidades_lista()
        return ctx

    def form_valid(self, form):
        try:
            contr_empr = self.obter_codigo_empresa_contexto(form=form)
            contr_fili = self.obter_codigo_filial_contexto(form=form)
            ContribuintesService.salvar_form(
                form=form,
                banco=self.request.banco,
                db_alias=self.db_alias,
                contr_empr=contr_empr,
                contr_fili=contr_fili,
            )
            messages.success(self.request, "Contribuinte atualizado com sucesso.")
            return redirect(reverse("contribuintes:listar") + f"?banco={self.request.banco}")
        except Exception as exc:
            messages.error(self.request, str(exc))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        return super().form_invalid(form)
