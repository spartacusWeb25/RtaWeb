from django.urls import path
from .listar import FolhaQuinzenalListView  

urlpatterns = [
    path('', FolhaQuinzenalListView.as_view(), name='folhaquinzenal_listar'),
]