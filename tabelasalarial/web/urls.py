from django.urls import path
from tabelasalarial.web.views.listar import TabelasalarialListView

urlpatterns = [
    path('', TabelasalarialListView.as_view(), name='tabelasalarial_listar'),
]