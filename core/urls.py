
from django.contrib import admin
from django.urls import path, include
from .views import HomeView
from licencas.views import LoginRtaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("folha/", include("folhamensal.urls")),
    path('home/', HomeView.as_view(), name="home"),
    path("licencas/", include("licencas.urls")),
    path("", LoginRtaView.as_view(), name="root"),
]
