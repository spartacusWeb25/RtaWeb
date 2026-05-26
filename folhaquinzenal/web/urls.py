from django.urls import path
from folhaquinzenal.web.views.listar import FolhaQuinzenalListView  

urlpatterns = [
    path('', FolhaQuinzenalListView.as_view(), name='folhaquinzenal_listar'),
]