from django.views.generic import ListView  
from setores.models import Setoresrh
from core.mixin import BancoObrigatorioMixin
from setores.services.listar import ListarSetoresrhService


class SetoresrhListView(BancoObrigatorioMixin, ListView):
    model = Setoresrh
    context_object_name = "setoresrh"
    template_name = "setores/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("referencia")
        empresa = self.request.GET.get("empresa")
        descricao = self.request.GET.get("descricao")
        codigo = self.request.GET.get("codigo")

        return ListarSetoresrhService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            empresa=empresa,
            referencia=referencia,
            descricao=descricao,
            codigo=codigo,
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["referencia"] = self.request.GET.get("referencia", "")
        context["empresa"] = self.request.GET.get("empresa", "")
        context["descricao"] = self.request.GET.get("descricao", "")
        context["codigo"] = self.request.GET.get("codigo", "")
        return context