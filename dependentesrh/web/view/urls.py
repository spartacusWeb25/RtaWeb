from django.urls import path
from .listar import DependentesRhListView

urlpatterns = [
    path('', DependentesRhListView.as_view(), name='dependentesrh_listar'),
]