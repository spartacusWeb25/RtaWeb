from django.urls import path
from empresas.web.views.criar import EmpresasCreateView
from empresas.web.views.deletar import EmpresasDeleteView
from empresas.web.views.editar import EmpresasUpdateView
from empresas.web.views.listar import EmpresasListView

app_name = "empresas"

urlpatterns = [
    path('', EmpresasListView.as_view(), name='listar'),
    path("criar/", EmpresasCreateView.as_view(), name="criar"),
    path(
        "<int:empresa>/<int:filial>/editar/",
        EmpresasUpdateView.as_view(),
        name="editar",
    ),
    path(
        "<int:empresa>/<int:filial>/deletar/",
        EmpresasDeleteView.as_view(),
        name="deletar",
    ),
]
