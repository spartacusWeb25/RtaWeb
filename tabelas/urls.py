
from django.urls import path
from tabelas.views.listView  import TabelaIrrfListView
from tabelas.views.listSql import TabelaIrrfSQLView



urlpatterns = [
    path("irrf/", TabelaIrrfListView.as_view(), name="irrf_list"),
    path("irrf-sql/", TabelaIrrfSQLView.as_view(), name="irrf_sql"),
]