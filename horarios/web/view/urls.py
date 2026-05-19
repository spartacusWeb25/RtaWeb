from django.urls import path
from .listar import HorarioListView
urlpatterns = [
    path('', HorarioListView.as_view(), name='horario_listar'),
]