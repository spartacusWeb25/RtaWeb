from django.urls import path
from .views.listar import SetoresrhListView
from .views.criar import SetoresCreateView
from .views.editar import SetoresrhUpdateView
from .views.deletar import SetoresrhDeleteView

app_name = "setores"



urlpatterns = [
    path("", SetoresrhListView.as_view(), name="setoresrh_listar"),
    path("criar/", SetoresCreateView.as_view(), name="setoresrh_criar"),
    path("editar/<str:empresa>/<str:codigo>/", SetoresrhUpdateView.as_view(), name="setoresrh_editar"),
    path("deletar/<str:empresa>/<str:codigo>/", SetoresrhDeleteView.as_view(), name="setoresrh_deletar"),
]