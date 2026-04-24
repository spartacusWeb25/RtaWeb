from django.urls import path
from .views import LoginRtaView

app_name = "licencas"

urlpatterns = [
    path("login/", LoginRtaView.as_view(), name="login"),
]