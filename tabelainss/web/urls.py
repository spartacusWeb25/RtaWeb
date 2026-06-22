from django.urls import path
from tabelainss.web.views.listar import TabelainssListView
from tabelainss.web.views.criar import TabelainssCreateView
from tabelainss.web.views.editar import TabelainssUpdateView
from tabelainss.web.views.deletar import TabelainssDeleteView

app_name = "tabelainss"

urlpatterns = [
    path('', TabelainssListView.as_view(), name='listar'),
    path("criar/", TabelainssCreateView.as_view(), name="inss_criar"),
    path("editar/<str:tabe_refe>/", TabelainssUpdateView.as_view(), name="inss_editar"),
    path("deletar/<str:tabe_refe>/", TabelainssDeleteView.as_view(), name="inss_deletar"),  
]
