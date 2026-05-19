from django.urls import path
from .listar import LancamentosfolhaListView
urlpatterns = [
    path('', LancamentosfolhaListView.as_view(), name='lancamentosfolha_listar'),
]