from django.urls import path
from lancamentosfolha.web.views.listar import LancamentosfolhaListView
urlpatterns = [
    path('', LancamentosfolhaListView.as_view(), name='lancamentosfolha_listar'),
]