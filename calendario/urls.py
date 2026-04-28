from django.urls import include, path

app_name = "calendario"

urlpatterns = [
    path("", include("calendario.Web.urls")),
]
