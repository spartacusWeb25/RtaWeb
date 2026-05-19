from django.urls import path
from .listar import SindicatoListView

urlpatterns = [
    path('', SindicatoListView.as_view(), name='sindicato_listar'),
]