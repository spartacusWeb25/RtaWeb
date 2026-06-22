from django.urls import path
from tabelasalariominimo.web.views.listar import TabelasalariominimoListView
from tabelasalariominimo.web.views.criar import TabelasalariominimoCreateView
from tabelasalariominimo.web.views.editar import TabelasalariominimoUpdateView
from tabelasalariominimo.web.views.deletar import TabelasalariominimoDeleteView

app_name = "tabelasalariominimo"

urlpatterns = [
    path('', TabelasalariominimoListView.as_view(), name='listar'),
    path("criar/", TabelasalariominimoCreateView.as_view(), name="salariominimo_criar"),
    path("editar/<str:refe_sala_mini>/", TabelasalariominimoUpdateView.as_view(), name="salariominimo_editar"),
    path("deletar/<str:refe_sala_mini>/", TabelasalariominimoDeleteView.as_view(), name="salariominimo_deletar"),
]
