from django.views.generic import ListView
from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from ...models import Empresas
from empresas.services.listar import ListarEmpresasService


class EmpresasListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Empresas
    template_name = "empresas/listar.html"
    context_object_name = "empresas"
    paginate_by = 20

    def get_queryset(self):
        referencia = self.request.GET.get("referencia")
        ordenar = self.request.GET.get("ordenar")

        return ListarEmpresasService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
            ordenar=ordenar,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["referencia"] = self.request.GET.get("referencia", "")
        context["ordenar"] = self.request.GET.get("ordenar", "")
        return context
