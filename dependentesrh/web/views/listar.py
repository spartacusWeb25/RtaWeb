from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from core.mixin import BancoObrigatorioMixin


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


class DependentesrhListView(BancoObrigatorioMixin, View):

    def get(self, request, *args, **kwargs):
        banco_limpo = _digits_only(request.banco)
        empr = request.GET.get("empresa") or request.GET.get("empr")
        fili = request.GET.get("filial") or request.GET.get("fili")
        func = request.GET.get("funcionario") or request.GET.get("func")
        if empr and fili and func:
            try:
                url = (
                    reverse(
                        "funcionarios:atualizar",
                        kwargs={
                            "func_empr": int(empr),
                            "func_fili": int(fili),
                            "func_codi": int(func),
                        },
                    )
                    + f"?banco={banco_limpo}#tab-parentes"
                )
                return redirect(url)
            except Exception:
                pass
        return redirect(reverse("funcionarios:listar") + f"?banco={banco_limpo}")
