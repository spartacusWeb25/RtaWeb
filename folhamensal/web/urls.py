from django.urls import path
from folhamensal.web.views.listar import FolhaMensalListView     
  

urlpatterns = [
    path('', FolhaMensalListView.as_view(), name='folhamensal_listar'),
]