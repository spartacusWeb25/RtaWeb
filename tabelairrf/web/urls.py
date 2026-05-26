from django.urls import path
from tabelairrf.web.views.listar import TabelairrfListView

urlpatterns = [
    path('', TabelairrfListView.as_view(), name='tabelairrf_listar'),
]