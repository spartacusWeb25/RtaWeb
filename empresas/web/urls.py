from django.urls import path
from empresas.web.views.listar import EmpresasListView

urlpatterns = [
    path('', EmpresasListView.as_view(), name='empresas_listar'),
]