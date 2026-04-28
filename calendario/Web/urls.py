from django.urls import path
from calendario.web.views import CalendarioEventoCreateView, CalendarioEventosJsonView

urlpatterns = [
    path("calendario/evento/criar/", CalendarioEventoCreateView.as_view(), name="evento_criar"),
    path("calendario/eventos/json/", CalendarioEventosJsonView.as_view(), name="eventos_json"),
]