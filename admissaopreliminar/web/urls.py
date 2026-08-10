from django.urls import path

from admissaopreliminar.web.views import AdmissaoPreliminarView

app_name = "admissaopreliminar"

urlpatterns = [
    path("", AdmissaoPreliminarView.as_view(), name="index"),
]
