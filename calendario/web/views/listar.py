from datetime import date

from django.http import JsonResponse
from django.views import View

from calendario.services import CalendarioService
from core.mixin import BancoObrigatorioMixin


class CalendarioEventosJsonView(BancoObrigatorioMixin, View):
    def get(self, request, *args, **kwargs):
        hoje = date.today()
        inicio_param = request.GET.get("inicio")
        fim_param = request.GET.get("fim")
        data_param = request.GET.get("data")
        somente_hoje = request.GET.get("somente_hoje") == "1"

        try:
            data_filtro = date.fromisoformat(data_param) if data_param else None
            data_inicio = date.fromisoformat(inicio_param) if inicio_param else None
            data_fim = date.fromisoformat(fim_param) if fim_param else None
        except ValueError:
            return JsonResponse({"erro": "Parâmetro de data inválido."}, status=400)

        if somente_hoje:
            eventos = CalendarioService.listar_eventos_do_dia(
                banco=request.banco,
                db_alias=request.db_alias,
                data=hoje,
            )
        elif data_filtro:
            eventos = CalendarioService.listar_eventos_do_dia(
                banco=request.banco,
                db_alias=request.db_alias,
                data=data_filtro,
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
            }
        )
