from django.urls import reverse
from django.views.generic import ListView

from departamentosrh.mixin import DepartamentoRhMixin
from departamentosrh.services.logic import _digits_only


class DepartamentoRhListView(DepartamentoRhMixin, ListView):
    model = None
    template_name = "departamentosrh/listar.html"
    context_object_name = "objetos"
    paginate_by = 50

    def get_queryset(self):
        # super().get_queryset() já filtra por registro, depa_empr=1 e depa_fili=1
        qs = super().get_queryset()
        busca = self.request.GET.get("busca", "").strip()
        ordem_raw = (self.request.GET.get("ordem", "") or "").strip().lower()
        ordem = ordem_raw if ordem_raw in ("asc", "desc") else "asc"
        self._ordem = ordem
        self._busca = busca
        if busca:
            from django.db.models import Q
            try:
                q_int = int(_digits_only(busca)) if _digits_only(busca).isdigit() else None
            except Exception:
                q_int = None
            q_cond = (
                Q(depa_desc__icontains=busca)
                | Q(depa_apelido__icontains=busca)
                | Q(depa_contab_codi__icontains=busca)
            )
            if q_int is not None:
                q_cond = q_cond | Q(depa_codi=q_int)
            qs = qs.filter(q_cond)
        # Ordem
        if ordem == "desc":
            qs = qs.order_by("-depa_codi")
        else:
            qs = qs.order_by("depa_codi")
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["busca"] = getattr(self, "_busca", "") or ""
        ctx["ordem"] = getattr(self, "_ordem", "asc") or "asc"
        ctx["titulo"] = "Departamentos"
        ctx["url_novo"] = reverse("departamentosrh:criar") + f"?banco={self.request.banco or ''}"
        ctx["url_buscar"] = reverse("departamentosrh:listar")
        ctx["proximo_codigo"] = None
        return ctx
