from core.mixin import BancoObrigatorioMixin as CoreBancoObrigatorioMixin


class BancoObrigatorioMixin(CoreBancoObrigatorioMixin):
    pass


def obter_codigo_empresa_contexto(request, form=None, instance=None):
    if form is not None:
        if form.is_bound:
            valor = form.data.get("depecontr_empr")
            if valor not in (None, ""):
                return valor
        valor = form.initial.get("depecontr_empr")
        if valor not in (None, ""):
            return valor

    if instance is not None:
        return getattr(instance, "depecontr_empr", "") or ""

    return request.GET.get("empr") or request.GET.get("empresa") or 1


def obter_codigo_filial_contexto(request, form=None, instance=None):
    if form is not None:
        if form.is_bound:
            valor = form.data.get("depecontr_fili")
            if valor not in (None, ""):
                return valor
        valor = form.initial.get("depecontr_fili")
        if valor not in (None, ""):
            return valor

    if instance is not None:
        return getattr(instance, "depecontr_fili", "") or 1

    return request.GET.get("fili") or request.GET.get("filial") or 1


def obter_codigo_contribuinte_contexto(request, form=None, instance=None):
    if form is not None:
        if form.is_bound:
            valor = form.data.get("depecontr_contr")
            if valor not in (None, ""):
                return valor
        valor = form.initial.get("depecontr_contr")
        if valor not in (None, ""):
            return valor

    if instance is not None:
        return getattr(instance, "depecontr_contr", "") or ""

    return request.GET.get("contr") or request.GET.get("contribuinte") or ""
