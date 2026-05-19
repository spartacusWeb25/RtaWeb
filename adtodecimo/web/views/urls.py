from django.urls import path
from .listar import AdtodecimoListView

urlpatterns = [
    path('', AdtodecimoListView.as_view(), name='adtodecimo_listar'),
]
