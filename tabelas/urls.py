from django.urls import path

from tabelas.views.listSql import TabelaIrrfSQLView
from tabelas.views.listView import (
    TabelaInssEmpresaListView,
    TabelaInssListView,
    TabelaIrrfListView,
)

urlpatterns = [
    path("inss/", TabelaInssListView.as_view(), name="inss_list"),
    path("inss-empresa/", TabelaInssEmpresaListView.as_view(), name="inss_empresa_list"),
    path("irrf/", TabelaIrrfListView.as_view(), name="irrf_list"),
    path("irrf-sql/", TabelaIrrfSQLView.as_view(), name="irrf_sql"),
]
