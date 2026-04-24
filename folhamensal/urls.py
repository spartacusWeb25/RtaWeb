from django.urls import path
from .views import FolhaMensalListView

app_name = "folha"

urlpatterns = [
    path("folha-mensal/", FolhaMensalListView.as_view(), name="folha_mensal_list"),
]