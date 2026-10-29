from types import SimpleNamespace

from django.urls import reverse
from django.views.generic import ListView

from aumento_salarial.mixin import AumentoSalarialMixin
from aumento_salarial.services.logic import AumentoSalarialService, _digits_only


class AumentoSalarialListView(AumentoSalarialMixin, ListView):
    model = None
    template_name = "aumento_salarial/listar.html"
    context_object_name = "objetos"
    paginate_by = 50

    def get_queryset(self):
        itens = AumentoSalarialService.listar(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=self.EMPRESA_FIXA_CODIGO,
            codigo_filial=self.FILIAL_FIXA_CODIGO,
        )
        busca = self.request.GET.get("busca", "").strip()
        ordem_raw = (self.request.GET.get("ordem", "") or "").strip().lower()
        ordem = ordem_raw if ordem_raw in ("asc", "desc") else "asc"
        self._ordem = ordem
        self._busca = busca
        if busca:
            busca_lower = busca.lower()
            busca_codigo = _digits_only(busca)
            busca_int = int(busca_codigo) if busca_codigo.isdigit() else None
            itens = [
                item for item in itens
                if (
                    (busca_int is not None and int(item.get("aume_codi") or 0) == busca_int)
                    or busca_lower in str(item.get("aume_desc") or "").lower()
                    or busca_lower in str(item.get("funcionario_nome") or "").lower()
                )
            ]
        itens = sorted(
            itens,
            key=lambda item: int(item.get("aume_codi") or 0),
            reverse=(ordem == "desc"),
        )
        return [SimpleNamespace(**item) for item in itens]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["busca"] = getattr(self, "_busca", "") or ""
        ctx["ordem"] = getattr(self, "_ordem", "asc") or "asc"
        ctx["titulo"] = "Aumento salarial"
        ctx["url_novo"] = reverse("aumento_salarial:criar") + f"?banco={self.request.banco or ''}"
        ctx["url_buscar"] = reverse("aumento_salarial:listar")
        return ctx
