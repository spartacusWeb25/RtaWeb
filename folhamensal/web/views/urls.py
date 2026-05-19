from django.urls import path
from .listar import FolhaMensalListView     

urlpatterns = [
    path('', FolhaMensalListView.as_view(), name='folhamensal_listar'),
]