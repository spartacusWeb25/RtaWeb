from django.urls import path
from adtodecimo.web.views.listar import AdtodecimoListView

app_name = 'adtodecimo'

urlpatterns = [
    path('', AdtodecimoListView.as_view(), name='adtodecimo_listar'),
]   