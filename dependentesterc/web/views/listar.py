from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from core.mixin import BancoObrigatorioMixin


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


class DependentestercListView(BancoObrigatorioMixin, View):

    def get(self, request, *args, **kwargs):
        banco_limpo = _digits_only(request.banco)
        empr = request.GET.get("empr") or request.GET.get("empresa")
        fili = request.GET.get("fili") or request.GET.get("filial")
        terc = request.GET.get("terc") or request.GET.get("terceiro")
        if empr and fili and terc:
            try:
                url = (
                    reverse(
                        "terceiros:atualizar",
                        kwargs={"empr": int(empr), "fili": int(fili), "codi": int(terc)},
                    )
                    + f"?banco={banco_limpo}#tab-dependentes"
                )
                return redirect(url)
            except Exception:
                pass
        return redirect(reverse("terceiros:listar") + f"?banco={banco_limpo}")
