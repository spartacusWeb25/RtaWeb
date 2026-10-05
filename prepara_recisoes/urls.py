from django.urls import path

from prepara_recisoes.web.views import criar
from prepara_recisoes.web.views import atualizar
from prepara_recisoes.web.views import listar
from prepara_recisoes.web.views import deletar

app_name = 'prepara_recisoes'

urlpatterns = [
    path('', listar.PreparaRescisoesListView.as_view(), name='listar'),
    path('criar/', criar.PreparaRescisoesCreateView.as_view(), name='criar'),

    # Padrão simplificado (empr=1/fili=1 implícitos)
    path('<int:prep_codi>/editar/',
         atualizar.PreparaRescisoesUpdateView.as_view(), name='editar'),
    path('<int:prep_codi>/excluir/',
         deletar.PreparaRescisoesDeleteView.as_view(), name='excluir'),

    # URLs compatíveis (empr/fili ignorados, sempre 1/1)
    path('<int:prep_empr>/<int:prep_fili>/<int:prep_codi>/editar/',
         atualizar.PreparaRescisoesUpdateView.as_view()),
    path('<int:prep_empr>/<int:prep_fili>/<int:prep_codi>/excluir/',
         deletar.PreparaRescisoesDeleteView.as_view()),
]
