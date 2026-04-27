from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class RootRedirectView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.session.get("usuario_id"):
            return redirect(reverse("home"))
        return redirect(reverse("licencas:login"))

import json
from pathlib import Path

from django.conf import settings


class AuditoriaLogsView(TemplateView):
    template_name = "core/auditoria_logs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.GET.get("usuario", "").strip().lower()
        metodo = self.request.GET.get("metodo", "").strip().upper()

        log_file = Path(settings.BASE_DIR) / "logs" / "http_audit.jsonl"
        rows = []

        if log_file.exists():
            for line in log_file.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if usuario and usuario not in str(item.get("usuario_nome", "")).lower():
                    continue
                if metodo and metodo != item.get("method", "").upper():
                    continue

                rows.append(item)

        context["logs"] = list(reversed(rows[-500:]))
        context["filtro_usuario"] = self.request.GET.get("usuario", "")
        context["filtro_metodo"] = self.request.GET.get("metodo", "")
        context["metodos"] = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        return context
