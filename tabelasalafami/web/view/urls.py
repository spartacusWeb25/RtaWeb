from django.urls import path
from .listar import TabelasalafamiListView

urlpatterns = [
    path('', TabelasalafamiListView.as_view(), name='tabelasalafami_listar'),
]