from django.http import HttpResponse
from django.views.generic import CreateView
from calendario.models import Calendariorh
from calendario.web.forms import CalendariorhForm
from django.urls import reverse_lazy

class CalendarioEventoCreateView(CreateView):
    model = Calendariorh
    form_class = CalendariorhForm
    template_name = 'calendario/criar.html'
    success_url = reverse_lazy('calendario:listar')
    
    def form_valid(self, form):
        form.instance.registro = self.request.user.registro
        return super().form_valid(form)
    
    
