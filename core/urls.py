from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import AuditoriaLogsView, HomeView, RootRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("folha/", include("folhamensal.urls")),
    path("funcionarios/", include("funcionarios.web.urls")),
    path('home/', HomeView.as_view(), name="home"),
    path("licencas/", include("licencas.urls")),
    path("licencas/usuarios/", include("licencas.web.urls")),
    path("tabelas/", include("tabelas.urls")),
    path("auditoria/logs/", AuditoriaLogsView.as_view(), name="auditoria_logs"),
    path("calendario/", include("calendario.urls")),
    path("", RootRedirectView.as_view(), name="root"),
]

# Em ambiente local, garante o serviço dos arquivos estáticos mesmo com DEBUG=False.
if settings.USE_LOCAL_DB or settings.DEBUG:
    static_root = settings.STATICFILES_DIRS[0] if getattr(settings, 'STATICFILES_DIRS', None) else settings.STATIC_ROOT
    urlpatterns += static(settings.STATIC_URL, document_root=static_root)
