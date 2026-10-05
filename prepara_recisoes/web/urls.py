from django.urls import include, path

urlpatterns = [
    path("", include("prepara_recisoes.urls")),
]
