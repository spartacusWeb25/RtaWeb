from django.urls import path

from departamentosrh.web.views import criar
from departamentosrh.web.views import atualizar
from departamentosrh.web.views import listar
from departamentosrh.web.views import deletar

app_name = 'departamentosrh'

urlpatterns = [
    path('', listar.DepartamentoRhListView.as_view(), name='listar'),
    path('criar/', criar.DepartamentoRhCreateView.as_view(), name='criar'),

    # URLs preferenciais (só depa_codi; empr=1 e fili=1 são implícitos)
    path('<int:depa_codi>/editar/',
         atualizar.DepartamentoRhUpdateView.as_view(), name='editar'),
    path('<int:depa_codi>/excluir/',
         deletar.DepartamentoRhDeleteView.as_view(), name='excluir'),

    # URLs compatíveis (empr/fili são ignorados, sempre 1/1)
    path('<int:depa_empr>/<int:depa_fili>/<int:depa_codi>/editar/',
         atualizar.DepartamentoRhUpdateView.as_view()),
    path('<int:depa_empr>/<int:depa_fili>/<int:depa_codi>/excluir/',
         deletar.DepartamentoRhDeleteView.as_view()),
]
