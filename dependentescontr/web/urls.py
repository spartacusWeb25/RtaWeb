from django.urls import path
from .views.listar import DependentescontrListView
from .views.criar import DependentescontrCreateView
from .views.atualizar import DependentescontrUpdateView
from .views.deletar import DependentescontrDeleteView

app_name = "dependentescontr"


urlpatterns = [
    path("", DependentescontrListView.as_view(), name="listar"),
    path("novo/", DependentescontrCreateView.as_view(), name="criar"),
    path("<str:empr>/<str:fili>/<str:contr>/<str:codi>/editar/", DependentescontrUpdateView.as_view(), name="atualizar"),
    path("<str:empr>/<str:fili>/<str:contr>/<str:codi>/excluir/", DependentescontrDeleteView.as_view(), name="deletar"),
]
