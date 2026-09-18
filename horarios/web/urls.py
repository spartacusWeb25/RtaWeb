from django.urls import path
from horarios.web.views import (
    HorarioListView,
    HorarioCreateView,
    HorarioUpdateView,
    HorarioDeleteView,
)

app_name = 'horarios'

urlpatterns = [
    path('', HorarioListView.as_view(), name='listar'),
    path('novo/', HorarioCreateView.as_view(), name='criar'),
    path('editar/<int:hora_codi>/', HorarioUpdateView.as_view(), name='editar'),
    path('excluir/<int:hora_codi>/', HorarioDeleteView.as_view(), name='excluir'),
]