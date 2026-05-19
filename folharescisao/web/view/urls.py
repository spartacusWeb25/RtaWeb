from django.urls import path
from .listar import FolhaRescisaoListView  

urlpatterns = [
    path('', FolhaRescisaoListView.as_view(), name='folharescisao_listar'),
]