from django.urls import path
from .views.listar import DependentestercListView
from .views.criar import DependentestercCreateView
from .views.atualizar import DependentestercUpdateView
from .views.deletar import DependentestercDeleteView

app_name = "dependentesterc"


urlpatterns = [
    path("", DependentestercListView.as_view(), name="listar"),
    path("novo/", DependentestercCreateView.as_view(), name="criar"),
    path("<int:empr>/<int:fili>/<int:terc>/<int:codi>/editar/", DependentestercUpdateView.as_view(), name="atualizar"),
    path("<int:empr>/<int:fili>/<int:terc>/<int:codi>/excluir/", DependentestercDeleteView.as_view(), name="deletar"),
]
