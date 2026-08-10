from django.views.generic import ListView  

from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from ...models import Funcionarios
from funcionarios.services.listar import ListarFuncionariosService   


class FuncionarioListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Funcionarios
    context_object_name = "funcionarios"
    template_name = "funcionarios/funcionarios_list.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("referencia")
        ordenar = self.request.GET.get("ordenar")

        return ListarFuncionariosService.listar(
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
