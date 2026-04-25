import json
from datetime import datetime
from pathlib import Path

from django.conf import settings

METHOD_LABEL = {
    "GET": "buscar/listar",
    "POST": "inserir",
    "PUT": "atualizar",
    "PATCH": "atualizar",
    "DELETE": "excluir",
}


class AuditoriaHttpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = Path(settings.BASE_DIR) / "logs" / "http_audit.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def __call__(self, request):
        response = self.get_response(request)

        payload = {}
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            payload = {
                k: v
                for k, v in request.POST.dict().items()
                if k.lower() not in {"csrfmiddlewaretoken", "password", "senha"}
            }

        row = {
            "ts": datetime.utcnow().isoformat(),
            "method": request.method,
            "method_label": METHOD_LABEL.get(request.method, request.method.lower()),
            "path": request.path,
            "query": request.GET.dict(),
            "payload": payload,
            "status_code": response.status_code,
            "usuario_id": request.session.get("usuario_id"),
            "usuario_nome": request.session.get("usuario_nome", "anonimo"),
            "banco": getattr(request, "banco", None),
            "ip": request.META.get("REMOTE_ADDR"),
        }

        with self.log_file.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(row, ensure_ascii=False) + "\n")

        return response
