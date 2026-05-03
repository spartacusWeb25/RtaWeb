from django.urls import path

from calendario.web.views.criar import CalendarioEventoCreateView
from calendario.web.views.listar import CalendarioEventosJsonView

app_name = "calendario_web"

urlpatterns = [
    path("eventos/json/", CalendarioEventosJsonView.as_view(), name="eventos_json"),
    path("eventos/novo/", CalendarioEventoCreateView.as_view(), name="evento_criar"),
]
