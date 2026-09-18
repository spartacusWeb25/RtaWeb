from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name="dispatch")
class PlanosQuadrosHorariosListarView(View):
    def get(self, request, *args, **kwargs):
        html = """
        <html><body style="font-family: Arial, sans-serif; padding: 40px; color:#444;">
        <h1 style="color:#0d6efd;">Planos de Quadros de Horários</h1>
        <p>Módulo em construção. Telas a serem implementadas em seguida.</p>
        <p><a href="javascript:history.back()">← Voltar</a></p>
        </body></html>
        """
        return HttpResponse(html)
