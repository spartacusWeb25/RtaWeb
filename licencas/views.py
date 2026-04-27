from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse

from .forms import LoginRtaForm
from .services import LoginRtaService


class LoginRtaView(View):
    template_name = "licencas/login.html"

    def get(self, request):
        return render(request, self.template_name, {
            "form": LoginRtaForm()
        })

    def post(self, request):
        form = LoginRtaForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Preencha todos os campos.")
            return render(request, self.template_name, {"form": form})

        ip = request.META.get("REMOTE_ADDR")

        ok, mensagem, dados = LoginRtaService.autenticar(
            registro=form.cleaned_data["registro"],
            usuario=form.cleaned_data["usuario"],
            senha=form.cleaned_data["senha"],
            ip=ip,
        )

        if not ok:
            messages.error(request, mensagem)
            return render(request, self.template_name, {"form": form})

        if "banco" not in dados or "usuario_id" not in dados:
            messages.error(request, "Dados incompletos.")
            return render(request, self.template_name, {"form": form})

        for chave, valor in dados.items():
            request.session[chave] = valor
        request.session.modified = True

        messages.success(request, mensagem)
        return redirect(reverse("home"))


class LogoutRtaView(View):
    def post(self, request):
        request.session.flush()
        messages.success(request, "Logout realizado com sucesso.")
        return redirect(reverse("licencas:login"))
