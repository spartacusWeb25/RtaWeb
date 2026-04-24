from django.http import JsonResponse

class BancoObrigatorioMixin:
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request, "banco", None):
            return JsonResponse({
                "erro": "Banco (registro) não informado"
            }, status=400)

        return super().dispatch(request, *args, **kwargs)