from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from licencas.views import LoginRtaView

from .views import AuditoriaLogsView, HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("folha/", include("folhamensal.urls")),
    path("funcionarios/", include("funcionarios.web.urls")),
    path('home/', HomeView.as_view(), name="home"),
    path("licencas/", include("licencas.urls")),
    path("auditoria/logs/", AuditoriaLogsView.as_view(), name="auditoria_logs"),
    path("", LoginRtaView.as_view(), name="root"),
]

# Em ambiente local, garante o serviço dos arquivos estáticos mesmo com DEBUG=False.
if settings.USE_LOCAL_DB or settings.DEBUG:
    static_root = settings.STATICFILES_DIRS[0] if getattr(settings, 'STATICFILES_DIRS', None) else settings.STATIC_ROOT
    urlpatterns += static(settings.STATIC_URL, document_root=static_root)
