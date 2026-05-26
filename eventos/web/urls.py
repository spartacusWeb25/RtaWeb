from django.urls import path
from eventos.web.views.listar import EventosListView    

urlpatterns = [
    path('', EventosListView.as_view(), name='eventos_listar'),
]