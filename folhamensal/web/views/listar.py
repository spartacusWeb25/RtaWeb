from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin
from folhamensal.models import Folhamensal
from folhamensal.services.listar import ListarFolhaMensalService

class FolhaMensalListView(BancoObrigatorioMixin, ListView):
    model = Folhamensal
    template_name = "folha/folha_mensal_list.html"
    context_object_name = "folhas"
    paginate_by = 25

    def get_queryset(self):
        return ListarFolhaMensalService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=self.request.GET.get("referencia"),
            empresa=self.request.GET.get("empresa"),
            filial=self.request.GET.get("filial"),
            funcionario=self.request.GET.get("funcionario"),
            evento=self.request.GET.get("evento"),
            ordenar=self.request.GET.get("ordenar"),
        )
        
        
