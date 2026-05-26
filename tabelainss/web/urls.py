from django.urls import path
from tabelainss.web.views.listar import TabelainssListView

urlpatterns = [
    path('', TabelainssListView.as_view(), name='tabelainss_listar'),
]