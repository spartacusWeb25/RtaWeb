from django.http import HttpResponse
from django.views.generic import ListView, View
from django.http import JsonResponse
from calendario.models import Calendariorh
class CalendarioListarListView(ListView):
    model = Calendariorh
    template_name = 'calendario/listar.html'
    context_object_name = 'calendarios'
    paginate_by = 10
    
    def get_queryset(self):
        return Calendariorh.objects.all()



class CalendarioEventosJsonView(View):
    def get(self, request, format=None):
        eventos = Calendariorh.objects.all()
        return JsonResponse(eventos, safe=False)
    
    def post(self, request, format=None):
        data = request.POST
        evento = Calendariorh.objects.create(**data)
        return JsonResponse(evento, safe=False)