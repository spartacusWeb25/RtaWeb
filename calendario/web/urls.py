from django.urls import path

from calendario.web.views.listar import CalendarioListarListView
from calendario.web.views.criar import CalendarioEventoCreateView
from calendario.web.views.listar import CalendarioEventosJsonView

urlpatterns = [
    path("eventos/json/", CalendarioEventosJsonView.as_view(), name="eventos_json"),
    path("eventos/novo/", CalendarioEventoCreateView.as_view(), name="evento_criar"),
    path("listar/", CalendarioListarListView.as_view(), name="listar"),
    
]
