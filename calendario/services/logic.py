from __future__ import annotations

from datetime import date
from django.db.models import QuerySet

from calendario.models import Calendariorh


class CalendarioService:
    @staticmethod
    def listar_eventos(*, banco: str, db_alias: str, data_inicio: date | None = None, data_fim: date | None = None) -> QuerySet[Calendariorh]:
        qs = Calendariorh.objects.using(db_alias).filter(registro=banco)

        if data_inicio:
            qs = qs.filter(cale_data__gte=data_inicio)
        if data_fim:
            qs = qs.filter(cale_data__lte=data_fim)

        return qs.order_by("cale_data", "cale_refe", "cale_cida")

    @staticmethod
    def listar_eventos_do_dia(*, banco: str, db_alias: str, data: date) -> QuerySet[Calendariorh]:
        return Calendariorh.objects.using(db_alias).filter(registro=banco, cale_data=data).order_by("cale_refe", "cale_cida")

    @staticmethod
    def salvar(*, instance: Calendariorh, db_alias: str) -> Calendariorh:
        instance.save(using=db_alias)
        return instance
