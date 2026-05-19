from datetime import date

from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.views.generic import ListView, View

from calendario.models import Calendariorh

from core.mixin import BancoObrigatorioMixin


class CalendarioListarListView(BancoObrigatorioMixin, ListView):
    model = Calendariorh
    template_name = 'calendario/listar.html'
    context_object_name = 'calendarios'
    paginate_by = 10
    
    def get_queryset(self):
        return (
            Calendariorh.objects.using(self.request.db_alias)
            .filter(registro=self.request.banco)
            .order_by("cale_data", "cale_cida")
        )



class CalendarioEventosJsonView(BancoObrigatorioMixin, View):
    def get(self, request, format=None):
        somente_hoje = str(request.GET.get("somente_hoje", "")).strip() in {"1", "true", "True"}

        inicio_raw = request.GET.get("inicio")
        fim_raw = request.GET.get("fim")
        inicio = parse_date(inicio_raw) if inicio_raw else None
        fim = parse_date(fim_raw) if fim_raw else None

        qs = Calendariorh.objects.using(request.db_alias).filter(registro=request.banco)

        if somente_hoje:
            qs = qs.filter(cale_data=date.today())
        else:
            if inicio and fim:
                qs = qs.filter(cale_data__range=(inicio, fim))
            elif inicio:
                qs = qs.filter(cale_data__gte=inicio)
            elif fim:
                qs = qs.filter(cale_data__lte=fim)

        eventos = []
        for row in qs.order_by("cale_data", "cale_cida").values(
            "cale_cida",
            "cale_refe",
            "cale_data",
            "cale_dia_desc",
        ):
            eventos.append(
                {
                    "codigo": row["cale_cida"],
                    "referencia": row["cale_refe"],
                    "data": row["cale_data"].isoformat() if row["cale_data"] else None,
                    "descanso": bool(row["cale_dia_desc"]),
                }
            )

        return JsonResponse({"eventos": eventos})
