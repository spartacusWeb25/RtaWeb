from django.urls import path
from .listar import EventosListView

urlpatterns = [
    path('', EventosListView.as_view(), name='eventos_listar'),
]