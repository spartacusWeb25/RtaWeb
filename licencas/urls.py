from django.urls import include, path

from .views import LoginRtaView

app_name = "licencas"

urlpatterns = [
    path("login/", LoginRtaView.as_view(), name="login"),
    path("usuarios/", include(("licencas.web.urls", "licencas"), namespace="licencas")),
]
