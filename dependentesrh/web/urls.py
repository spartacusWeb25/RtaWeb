from django.urls import path
from dependentesrh.web.views.listar import DependentesRhListView    

urlpatterns = [
    path('', DependentesRhListView.as_view(), name='dependentesrh_listar'),
]