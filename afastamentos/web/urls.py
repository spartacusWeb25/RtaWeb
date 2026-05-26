from django.urls import path
from afastamentos.web.views.listar import AfastamentosListView  

urlpatterns = [
    path('', AfastamentosListView.as_view(), name='afastamentos_listar'),
]