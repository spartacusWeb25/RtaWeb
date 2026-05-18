from folhamensal.models import Folhamensal

from .criar import FolhaMensalEditarService, FolhaMensalRemoverService, FolhaMensalSalvarService


class FolhaMensalService:
    @staticmethod
    def buscar_unico(*, banco, db_alias, fome_empr, fome_fili, fome_func, fome_refe, fome_even):
        return FolhaMensalEditarService.buscar_unico(
            banco=banco,
            db_alias=db_alias,
            fome_empr=fome_empr,
            fome_fili=fome_fili,
            fome_func=fome_func,
            fome_refe=fome_refe,
            fome_even=fome_even,
        )

    @staticmethod
    def salvar(*, instance: Folhamensal, db_alias: str) -> Folhamensal:
        return FolhaMensalSalvarService.salvar(instance=instance, db_alias=db_alias)

    @staticmethod
    def remover(*, instance: Folhamensal, db_alias: str) -> None:
        FolhaMensalRemoverService.remover(instance=instance, db_alias=db_alias)
        
  
