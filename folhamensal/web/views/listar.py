from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin
from folhamensal.models import Folhamensal
from folhamensal.services import FolhaMensalService


class FolhaMensalListView(BancoObrigatorioMixin, ListView):
    model = Folhamensal
    template_name = "folha/folha_mensal_list.html"
    context_object_name = "folhas"
    paginate_by = 50

    def get_queryset(self):
        return FolhaMensalService.listar(
            banco=self.request.banco,
            referencia=self.request.GET.get("referencia"),
            empresa=self.request.GET.get("empresa"),
            filial=self.request.GET.get("filial"),
            funcionario=self.request.GET.get("funcionario"),
        )