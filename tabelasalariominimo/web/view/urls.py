from django.urls import path
from .listar import TabelasalariominimoListView

urlpatterns = [
    path('', TabelasalariominimoListView.as_view(), name='tabelasalariominimo_listar'),
]