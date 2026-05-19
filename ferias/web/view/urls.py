from django.urls import path
from .listar import FeriasListView

urlpatterns = [
    path('', FeriasListView.as_view(), name='ferias_listar'),
]