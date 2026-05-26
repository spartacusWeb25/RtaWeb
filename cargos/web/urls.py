from django.urls import path
from cargos.web.views.listar import CargosListView

urlpatterns = [
    path('', CargosListView.as_view(), name='cargos_listar'),
]