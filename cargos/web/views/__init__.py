from cargos.web.views.listar import CargosListView
from cargos.web.views.criar import CargoCreateView
from cargos.web.views.atualizar import CargoUpdateView
from cargos.web.views.deletar import CargoDeleteView

CargosListarView = CargosListView
CargosCriarView = CargoCreateView
CargosAtualizarView = CargoUpdateView
CargosDeletarView = CargoDeleteView

__all__ = [
    "CargosListView",
    "CargoCreateView",
    "CargoUpdateView",
    "CargoDeleteView",
    "CargosListarView",
    "CargosCriarView",
    "CargosAtualizarView",
    "CargosDeletarView",
]
