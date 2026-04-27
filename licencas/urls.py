from django.urls import include, path

from .views import LoginRtaView, LogoutRtaView

app_name = "licencas"

urlpatterns = [
    path("login/", LoginRtaView.as_view(), name="login"),
    path("logout/", LogoutRtaView.as_view(), name="logout"),
   
]
