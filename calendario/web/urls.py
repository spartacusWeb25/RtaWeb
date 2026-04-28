from django.urls import path
from calendario.web.views.criar import CalendarioEventoCreateView
from calendario.web.views.listar import CalendarioEventosJsonView

urlpatterns = [
    path("calendario/evento/criar/", CalendarioEventoCreateView.as_view(), name="evento_criar"),
    path("calendario/eventos/json/", CalendarioEventosJsonView.as_view(), name="eventos_json"),
]