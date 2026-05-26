from django.urls import path
from ferias.web.views.listar import FeriasListView

urlpatterns = [
    path('', FeriasListView.as_view(), name='ferias_listar'),
]