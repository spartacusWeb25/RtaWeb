from django.urls import reverse
from django.views.generic import ListView

from prepara_recisoes.mixin import PreparaRescisoesMixin
from prepara_recisoes.services.logic import _digits_only


class PreparaRescisoesListView(PreparaRescisoesMixin, ListView):
    model = None
    template_name = "prepara_rescisoes/listar.html"
    context_object_name = "objetos"
    paginate_by = 50

    def get_queryset(self):
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
                Q(prep_desc__icontains=busca)
                | Q(prep_descricao__icontains=busca)
                | Q(prep_aviso_previo_desc__icontains=busca)
                | Q(prep_iniciativa_desc__icontains=busca)
                | Q(prep_saque_desc__icontains=busca)
                | Q(prep_caged_desc__icontains=busca)
                | Q(prep_rais_desc__icontains=busca)
                | Q(prep_motivo_esocial_desc__icontains=busca)
                | Q(prep_homolognet_desc__icontains=busca)
            )
            if q_int is not None:
                q_cond = q_cond | Q(prep_codi=q_int)
            qs = qs.filter(q_cond)
        if ordem == "desc":
            qs = qs.order_by("-prep_codi")
        else:
            qs = qs.order_by("prep_codi")
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["busca"] = getattr(self, "_busca", "") or ""
        ctx["ordem"] = getattr(self, "_ordem", "asc") or "asc"
        ctx["titulo"] = "Preparação de Rescisões"
        ctx["url_novo"] = reverse("prepara_recisoes:criar") + f"?banco={self.request.banco or ''}"
        ctx["url_buscar"] = reverse("prepara_recisoes:listar")
        ctx["proximo_codigo"] = None
        return ctx
