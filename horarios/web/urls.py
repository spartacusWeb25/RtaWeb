from django.urls import path
from horarios.web.views.listar import HorarioListView
urlpatterns = [
    path('', HorarioListView.as_view(), name='horario_listar'),
]