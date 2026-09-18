from django.urls import path
from cargos.web.views.listar import CargosListView
from cargos.web.views.criar import CargoCreateView
from cargos.web.views.atualizar import CargoUpdateView
from cargos.web.views.deletar import CargoDeleteView

app_name = 'cargos'

urlpatterns = [
    path('', CargosListView.as_view(), name='listar'),
    path('novo/', CargoCreateView.as_view(), name='criar'),
    path('<int:empr>/<int:fili>/<int:codi>/editar/', CargoUpdateView.as_view(), name='editar'),
    path('<int:empr>/<int:fili>/<int:codi>/excluir/', CargoDeleteView.as_view(), name='excluir'),
]
