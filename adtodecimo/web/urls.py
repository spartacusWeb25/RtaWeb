from django.urls import path
from adtodecimo.web.views.listar import AdtodecimoListView

urlpatterns = [
    path('', AdtodecimoListView.as_view(), name='adtodecimo_listar'),
]   