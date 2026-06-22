from django.urls import path

from tabelainss.web.views.listar import TabelainssListView
from tabelairrf.web.views.listar import TabelairrfListView
from tabelas.views.listSql import TabelaIrrfSQLView
from tabelas.views.listView import (
    TabelaInssEmpresaListView,
)

urlpatterns = [
    path("inss/", TabelainssListView.as_view(), name="inss_list"),
    path("inss-empresa/", TabelaInssEmpresaListView.as_view(), name="inss_empresa_list"),
    path("irrf/", TabelairrfListView.as_view(), name="irrf_list"),
    path("irrf-sql/", TabelaIrrfSQLView.as_view(), name="irrf_sql"),
]
