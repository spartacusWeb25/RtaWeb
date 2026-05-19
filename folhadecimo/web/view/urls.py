from django.urls import path
from .listar import FolhadecimoListView

urlpatterns = [
    path('', FolhadecimoListView.as_view(), name='folhadecimo_listar'),
]