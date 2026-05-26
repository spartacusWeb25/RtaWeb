from django.urls import path
from folhaadtodecimo.web.views.listar import FolhaAdtodecimoListView        

urlpatterns = [
    path('', FolhaAdtodecimoListView.as_view(), name='folhaadtodecimo_listar'),
]