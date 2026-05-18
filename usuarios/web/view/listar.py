from django.views.generic import ListView  

from core.mixin import BancoObrigatorioMixin
from ...models import Usuarios
from usuarios.services.listar import ListarUsuariosService   
  
        
class UsuariosListView(BancoObrigatorioMixin, ListView):
    model = Usuarios
    context_object_name = "usuarios"
    template_name = "usuarios/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarUsuariosService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        
