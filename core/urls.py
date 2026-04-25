
from django.contrib import admin
from django.urls import path, include
from .views import HomeView, AuditoriaLogsView
from licencas.views import LoginRtaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("folha/", include("folhamensal.urls")),
    path("funcionarios/", include("funcionarios.web.urls")),
    path('home/', HomeView.as_view(), name="home"),
    path("licencas/", include("licencas.urls")),
    path("auditoria/logs/", AuditoriaLogsView.as_view(), name="auditoria_logs"),
    path("", LoginRtaView.as_view(), name="root"),
]
