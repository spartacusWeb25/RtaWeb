from django.urls import path
from .listar import FolhaAdtodecimoListView

urlpatterns = [
    path('', FolhaAdtodecimoListView.as_view(), name='folhaadtodecimo_listar'),
]