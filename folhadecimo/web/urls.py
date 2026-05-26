from django.urls import path
from folhadecimo.web.views.listar import FolhadecimoListView    

urlpatterns = [
    path('', FolhadecimoListView.as_view(), name='folhadecimo_listar'),
]