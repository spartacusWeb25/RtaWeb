from django.urls import path
from sindicatos.web.views.listar import SindicatoListView
from sindicatos.web.views.criar import SindicatoTrabalhadoresCreateView
from sindicatos.web.views.atualizar import SindicatoTrabalhadoresUpdateView
from sindicatos.web.views.deletar import SindicatoTrabalhadoresDeleteView

app_name = "sindicatos"

urlpatterns = [
    path('', SindicatoListView.as_view(), name='listar'),
    path('novo/', SindicatoTrabalhadoresCreateView.as_view(), name='criar'),
    path('<int:empr>/<int:fili>/<int:codi>/editar/', SindicatoTrabalhadoresUpdateView.as_view(), name='atualizar'),
    path('<int:empr>/<int:fili>/<int:codi>/excluir/', SindicatoTrabalhadoresDeleteView.as_view(), name='deletar'),
]
