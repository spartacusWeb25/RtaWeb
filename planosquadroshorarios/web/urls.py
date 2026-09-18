from django.urls import path
from planosquadroshorarios.web.views.listar import PlanosQuadrosHorariosListarView

app_name = "planosquadroshorarios"

urlpatterns = [
    path("", PlanosQuadrosHorariosListarView.as_view(), name="listar"),
]
