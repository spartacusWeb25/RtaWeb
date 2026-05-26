from django.urls import path
from folharescisao.web.views.listar import FolhaRescisaoListView  

urlpatterns = [
    path('', FolhaRescisaoListView.as_view(), name='folharescisao_listar'),
]