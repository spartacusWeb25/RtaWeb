from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import AuditoriaLogsView, HomeView, RootRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("folhamensal/", include("folhamensal.web.urls")),
    path("funcionarios/", include("funcionarios.web.urls")),
    path('home/', HomeView.as_view(), name="home"),
    path("licencas/", include("licencas.urls")),
    path("licencas/usuarios/", include("licencas.web.urls")),
    path("tabelas/", include("tabelas.urls")),
    path("auditoria/logs/", AuditoriaLogsView.as_view(), name="auditoria_logs"),
    path("calendario/", include("calendario.urls")),
    path("", RootRedirectView.as_view(), name="root"),
    path("adtodecimo/", include("adtodecimo.web.urls")),
    path("afastamentos/", include("afastamentos.web.urls")),
    path("cargos/", include("cargos.web.urls")),
    path("dadosrescisao/", include("dadosrescisao.web.urls")),
    path("dependentesrh/", include("dependentesrh.web.urls")),
    path("empresas/", include("empresas.web.urls")),
    path("eventos/", include("eventos.web.urls")),
    path("ferias/", include("ferias.web.urls")),
    path("folhaadtodecimo/", include("folhaadtodecimo.web.urls")),
    path("folhadecimo/", include("folhadecimo.web.urls")),
    path("folhaquinzenal/", include("folhaquinzenal.web.urls")),
    path("folharescisao/", include("folharescisao.web.urls")),
    path("horarios/", include("horarios.web.urls")),
    path("lancamentosfolha/", include("lancamentosfolha.web.urls")),
    path("sindicatos/", include("sindicatos.web.urls")),
    path("tabelainss/", include("tabelainss.web.urls")),
    path("tabelairrf/", include("tabelairrf.web.urls")),
    path("tabelasalafami/", include("tabelasalafami.web.urls")),
    path("tabelasalarial/", include("tabelasalarial.web.urls")),
    path("tabelasalariominimo/", include("tabelasalariominimo.web.urls")),
    path("usuarios/", include("usuarios.web.urls")),
]

# Em ambiente local, garante o serviço dos arquivos estáticos mesmo com DEBUG=False.
if settings.USE_LOCAL_DB or settings.DEBUG:
    static_root = settings.STATICFILES_DIRS[0] if getattr(settings, 'STATICFILES_DIRS', None) else settings.STATIC_ROOT
    urlpatterns += static(settings.STATIC_URL, document_root=static_root)
