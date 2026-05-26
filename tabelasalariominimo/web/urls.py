from django.urls import path
from tabelasalariominimo.web.views.listar import TabelasalariominimoListView

app_name = "tabelasalariominimo"

urlpatterns = [
    path('', TabelasalariominimoListView.as_view(), name='listar'),
]