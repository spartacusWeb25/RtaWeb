from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView, TemplateView,
)
from django.contrib import messages
from django.core.exceptions import ValidationError
from core.mixin import BancoObrigatorioMixin

from horarios.mixin import HorariosMixin
from horarios.models import Horarios
from horarios.web.forms import HorariosForm
from horarios.services.logic import HorariosService
from horarios.services.listar import ListarHorariosService


def _todos_campos_iniciais():
    keys = [
        "registro", "hora_empr", "hora_fili", "hora_codi",
        "hora_nome", "hora_flexivel", "hora_total_semana",
        "hora_folga_alt",
        "hora_folga_dom", "hora_folga_seg", "hora_folga_ter",
        "hora_folga_qua", "hora_folga_qui", "hora_folga_sex", "hora_folga_sab",
        "hora_desc_esocial",
    ]
    dias = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"]
    campos_hora = [
        "esoc",
        "inic_1", "fina_1",
        "lanc_inic_1", "lanc_fina_1",
        "inic_2", "fina_2",
        "lanc_inic_2", "lanc_fina_2",
        "intervalo", "jornada",
    ]
    for d in dias:
        for c in campos_hora:
            keys.append(f"hora_{d}_{c}")
    return keys


class HorarioListView(BancoObrigatorioMixin, HorariosMixin, ListView):
    model = Horarios
    context_object_name = "horarios"
    template_name = "horarios/listar.html"
    paginate_by = 30

    def get_queryset(self):
        busca = self.request.GET.get("busca")
        ordenar = self.request.GET.get("ordenar")
        return ListarHorariosService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            busca=busca,
            ordenar=ordenar,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["busca_valor"] = self.request.GET.get("busca", "") or ""
        ctx["ordenar_valor"] = self.request.GET.get("ordenar", "asc") or "asc"
        return ctx


class HorarioCreateView(BancoObrigatorioMixin, HorariosMixin, CreateView):
    model = Horarios
    form_class = HorariosForm
    template_name = "horarios/form.html"
    success_url_name = "horarios:listar"

    def get_initial(self):
        initial = super().get_initial() or {}
        banco = getattr(self.request, "banco", "")
        from horarios.services.logic import _digits_only, _safe_int
        banco_limpo = _digits_only(banco)
        proximo = HorariosService.proximo_codigo_quadro(
            banco=banco,
            db_alias=getattr(self.request, "db_alias", "default"),
            empr_codigo=1,
            fili_codigo=1,
        )
        initial.setdefault("registro", banco_limpo)
        initial.setdefault("hora_empr", 1)
        initial.setdefault("hora_fili", 1)
        initial.setdefault("hora_codi", proximo)
        for chave in _todos_campos_iniciais():
            if chave not in initial:
                if chave.startswith("hora_folga_") or chave in ("hora_flexivel", "hora_folga_alt"):
                    initial[chave] = False
                elif chave.endswith("_esoc"):
                    initial[chave] = None
                else:
                    initial[chave] = ""
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object"] = None
        return ctx

    def form_valid(self, form):
        try:
            HorariosService.salvar_form(
                form=form,
                operacao="criar",
                banco=self.request.banco,
                db_alias=self.request.db_alias,
                empr_codigo=1,
                fili_codigo=1,
            )
        except ValidationError as exc:
            for msg in exc.messages:
                form.add_error(None, msg)
            return self.form_invalid(form)
        messages.success(self.request, "Quadro de horários criado com sucesso!")
        banco = getattr(self.request, "banco", "")
        return redirect(f"{reverse('horarios:listar')}?banco={banco}")

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Revise os campos destacados em vermelho antes de salvar.",
        )
        return super().form_invalid(form)


class HorarioUpdateView(BancoObrigatorioMixin, HorariosMixin, UpdateView):
    model = Horarios
    form_class = HorariosForm
    template_name = "horarios/form.html"
    success_url_name = "horarios:listar"

    def get_object(self, queryset=None):
        banco = getattr(self.request, "banco", "")
        from horarios.services.logic import _digits_only, _safe_int
        banco_limpo = _digits_only(banco)
        hora_codi = _safe_int(self.kwargs.get("hora_codi"))
        obj = get_object_or_404(
            Horarios.objects.using(getattr(self.request, "db_alias", "default")),
            registro=banco_limpo,
            hora_empr=1,
            hora_fili=1,
            hora_codi=hora_codi,
        )
        return obj

    def get_initial(self):
        initial = super().get_initial() or {}
        obj = getattr(self, "object", None)
        if obj is None:
            obj = getattr(self, "get_object", None)
            if obj is not None:
                try:
                    obj = self.get_object()
                except Exception:
                    obj = None
        if obj is not None:
            for chave in _todos_campos_iniciais():
                if chave in ("registro", "hora_empr", "hora_fili", "hora_codi"):
                    continue
                try:
                    val = getattr(obj, chave, None)
                except Exception:
                    val = None
                if chave in initial:
                    continue
                if val is None or val == "":
                    if chave.startswith("hora_folga_") or chave in ("hora_flexivel", "hora_folga_alt"):
                        initial[chave] = False
                    elif chave.endswith("_esoc"):
                        initial[chave] = None
                    else:
                        initial[chave] = ""
                else:
                    initial[chave] = val
        for chave in _todos_campos_iniciais():
            if chave not in initial:
                if chave.startswith("hora_folga_") or chave in ("hora_flexivel", "hora_folga_alt"):
                    initial[chave] = False
                elif chave.endswith("_esoc"):
                    initial[chave] = None
                else:
                    initial[chave] = ""
        return initial

    def form_valid(self, form):
        try:
            HorariosService.salvar_form(
                form=form,
                operacao="editar",
                banco=self.request.banco,
                db_alias=self.request.db_alias,
                empr_codigo=1,
                fili_codigo=1,
            )
        except ValidationError as exc:
            for msg in exc.messages:
                form.add_error(None, msg)
            return self.form_invalid(form)
        messages.success(self.request, "Quadro de horários atualizado com sucesso!")
        banco = getattr(self.request, "banco", "")
        return redirect(f"{reverse('horarios:listar')}?banco={banco}")

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Revise os campos destacados em vermelho antes de salvar.",
        )
        return super().form_invalid(form)


class HorarioDeleteView(BancoObrigatorioMixin, HorariosMixin, DeleteView):
    model = Horarios
    template_name = "horarios/confirmar_exclusao.html"
    success_url = reverse_lazy("horarios:listar")

    def get_object(self, queryset=None):
        banco = getattr(self.request, "banco", "")
        from horarios.services.logic import _digits_only, _safe_int
        banco_limpo = _digits_only(banco)
        hora_codi = _safe_int(self.kwargs.get("hora_codi"))
        obj = get_object_or_404(
            Horarios.objects.using(getattr(self.request, "db_alias", "default")),
            registro=banco_limpo,
            hora_empr=1,
            hora_fili=1,
            hora_codi=hora_codi,
        )
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = ctx.get("object")
        nome = "Quadro de Horários"
        if obj is not None:
            n = getattr(obj, "hora_nome", None) or ""
            codi = getattr(obj, "hora_codi", None)
            if n:
                nome = n
            elif codi:
                nome = f"Quadro #{codi}"
        ctx["objeto_desc"] = nome
        return ctx

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        db_alias = getattr(request, "db_alias", "default")
        try:
            self.object.delete(db_alias=db_alias)
        except TypeError:
            self.object.delete()
        messages.success(request, "Quadro de horários excluído com sucesso!")
        banco = getattr(request, "banco", "")
        return redirect(f"{reverse('horarios:listar')}?banco={banco}")
