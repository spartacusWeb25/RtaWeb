from django.urls import path
from tabelasalafami.web.views.listar import TabelasalafamiListView
from tabelasalafami.web.views.criar import TabelasalafamiCreateView
from tabelasalafami.web.views.editar import TabelasalafamiUpdateView
from tabelasalafami.web.views.deletar import TabelasalafamiDeleteView



app_name = "tabelasalafami"



urlpatterns = [
    path('', TabelasalafamiListView.as_view(), name='salafami_listar'),
    path("criar/", TabelasalafamiCreateView.as_view(), name="salafami_criar"),
    path("editar/<str:empresa>/<str:codigo>/", TabelasalafamiUpdateView.as_view(), name="salafami_editar"),
    path("deletar/<str:empresa>/<str:codigo>/", TabelasalafamiDeleteView.as_view(), name="salafami_deletar"), 
]