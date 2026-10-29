from django.urls import include, path

urlpatterns = [
    path("", include("prepara_rescisoes.urls")),
]
