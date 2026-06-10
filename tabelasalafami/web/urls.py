from django.urls import path
from tabelasalafami.web.views.listar import TabelasalafamiListView


app_name = "tabelasalafami"



urlpatterns = [
    path('', TabelasalafamiListView.as_view(), name='salafami_listar'),
]