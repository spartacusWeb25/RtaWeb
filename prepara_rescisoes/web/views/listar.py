from django.urls import reverse
from django.views.generic import ListView
from types import SimpleNamespace

from prepara_rescisoes.mixin import PreparaRescisoesMixin
from prepara_rescisoes.services.logic import PreparaRescisoesService, _digits_only


class PreparaRescisoesListView(PreparaRescisoesMixin, ListView):
    model = None
    template_name = "prepara_rescisoes/listar.html"
    context_object_name = "objetos"
    paginate_by = 50

    def get_queryset(self):
        itens = PreparaRescisoesService.listar(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=self.EMPRESA_FIXA_CODIGO,
            codigo_filial=self.FILIAL_FIXA_CODIGO,
            incluir_inativos=True,
        )
        busca = self.request.GET.get("busca", "").strip()
        ordem_raw = (self.request.GET.get("ordem", "") or "").strip().lower()
        ordem = ordem_raw if ordem_raw in ("asc", "desc") else "asc"
        self._ordem = ordem
        self._busca = busca
        if busca:
            try:
                q_int = int(_digits_only(busca)) if _digits_only(busca).isdigit() else None
            except Exception:
                q_int = None
            busca_lower = busca.lower()
            itens = [
                item for item in itens
                if (
                    (q_int is not None and int(item.get("prep_codi") or 0) == q_int)
                    or busca_lower in str(item.get("prep_desc", "")).lower()
                    or busca_lower in str(item.get("prep_descricao", "")).lower()
                    
                )
            ]
        itens = sorted(
            itens,
            key=lambda item: int(item.get("prep_codi") or 0),
            reverse=(ordem == "desc"),
        )
        return [SimpleNamespace(**item) for item in itens]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["busca"] = getattr(self, "_busca", "") or ""
        ctx["ordem"] = getattr(self, "_ordem", "asc") or "asc"
        ctx["titulo"] = "Preparação de Rescisões"
        ctx["url_novo"] = reverse("prepara_rescisoes:criar") + f"?banco={self.request.banco or ''}"
        ctx["url_buscar"] = reverse("prepara_rescisoes:listar")
        ctx["proximo_codigo"] = None
        return ctx
