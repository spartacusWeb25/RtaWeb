from django.urls import path
from afastamentos.web.views.listar import AfastamentosListView  

app_name = 'afastamentos'

urlpatterns = [
    path('', AfastamentosListView.as_view(), name='afastamentos_listar'),
]