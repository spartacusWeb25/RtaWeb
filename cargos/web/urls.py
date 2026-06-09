from django.urls import path
from cargos.web.views.listar import CargosListView

app_name = 'cargos'

urlpatterns = [
    path('', CargosListView.as_view(), name='cargos_listar'),
]