from django.urls import path
from sindicatos.web.views.listar import SindicatoListView   

urlpatterns = [
    path('', SindicatoListView.as_view(), name='sindicato_listar'),
]