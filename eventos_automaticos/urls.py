from django.urls import path

from eventos_automaticos.web.views.listar import EventosAutomaticosListView


app_name = "eventos_automaticos"

urlpatterns = [
    path("", EventosAutomaticosListView.as_view(), name="listar"),
]
