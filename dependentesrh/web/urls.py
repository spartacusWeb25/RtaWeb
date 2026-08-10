from django.urls import path
from .views.listar import DependentesrhListView
from .views.criar import DependentesCreateView
from .views.editar import DependentesrhUpdateView
from .views.deletar import DependentesrhDeleteView

app_name = "dependentesrh"


urlpatterns = [
    path("", DependentesrhListView.as_view(), name="listar"),
    path("criar/", DependentesCreateView.as_view(), name="criar"),
    path("editar/<str:empresa>/<str:filial>/<str:funcionario>/<str:codigo>/", DependentesrhUpdateView.as_view(), name="editar"),
    path("deletar/<str:empresa>/<str:filial>/<str:funcionario>/<str:codigo>/", DependentesrhDeleteView.as_view(), name="deletar"),
]
