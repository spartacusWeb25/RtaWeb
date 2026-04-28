from datetime import date

from django.http import JsonResponse
from django.views import View

from core.mixin import BancoObrigatorioMixin
from calendario.services import CalendarioService


class CalendarioEventosJsonView(BancoObrigatorioMixin, View):
    def get(self, request, *args, **kwargs):
        hoje = date.today()
        inicio_param = request.GET.get("inicio")
        fim_param = request.GET.get("fim")
        somente_hoje = request.GET.get("somente_hoje") == "1"

        data_inicio = date.fromisoformat(inicio_param) if inicio_param else None
        data_fim = date.fromisoformat(fim_param) if fim_param else None

        if somente_hoje:
            eventos = CalendarioService.listar_eventos_do_dia(
                banco=request.banco,
                db_alias=request.db_alias,
                data=hoje,
            )
        else:
            eventos = CalendarioService.listar_eventos(
                banco=request.banco,
                db_alias=request.db_alias,
                data_inicio=data_inicio,
                data_fim=data_fim,
            )

        payload = [
            {
                "registro": evento.registro,
                "codigo": evento.cale_cida,
                "referencia": evento.cale_refe,
                "data": evento.cale_data.isoformat(),
                "descanso": bool(evento.cale_dia_desc),
            }
            for evento in eventos
        ]

        return JsonResponse(
            {
                "eventos": payload,
                "total": len(payload),
                "hoje": hoje.isoformat(),
                "tem_eventos_hoje": any(item["data"] == hoje.isoformat() for item in payload),
            }
        )
