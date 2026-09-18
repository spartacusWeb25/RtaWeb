from django.urls import path
from planoscargos.web.views.listar import PlanosCargosListarView

app_name = "planoscargos"

urlpatterns = [
    path("", PlanosCargosListarView.as_view(), name="listar"),
]
