from core.mixin import BancoObrigatorioMixin
from eventos_automaticos.services.logic import (
    EventosAutomaticosService,
    TIPO_CALCULO_DEFAULT,
    TIPO_CALCULO_LABELS,
    _digits_only,
)


class EventosAutomaticosMixin(BancoObrigatorioMixin):
    EMPRESA_FIXA_CODIGO = 1
    FILIAL_FIXA_CODIGO = 1

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        request.empr_padrao_cod = self.EMPRESA_FIXA_CODIGO
        request.fili_padrao_cod = self.FILIAL_FIXA_CODIGO
        return result

    @property
    def banco_limpo(self):
        return _digits_only(getattr(self.request, "banco", "") or "")

    @property
    def db_alias(self):
        return getattr(self.request, "db_alias", None) or "default"

    @property
    def aba_ativa(self):
        valor = self.request.POST.get("aba") or self.request.GET.get("aba") or TIPO_CALCULO_DEFAULT
        valor = str(valor or "").strip()
        if valor in TIPO_CALCULO_LABELS:
            return valor
        return TIPO_CALCULO_DEFAULT

    def obter_codigo_empresa_contexto(self):
        return self.EMPRESA_FIXA_CODIGO

    def obter_codigo_filial_contexto(self):
        return self.FILIAL_FIXA_CODIGO

    def obter_nome_empresa_contexto(self):
        return EventosAutomaticosService.obter_nome_empresa(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=self.EMPRESA_FIXA_CODIGO,
        )

    def obter_nome_filial_contexto(self):
        return EventosAutomaticosService.obter_nome_filial(
            banco=self.banco_limpo,
            db_alias=self.db_alias,
            codigo_empresa=self.EMPRESA_FIXA_CODIGO,
            codigo_filial=self.FILIAL_FIXA_CODIGO,
        )
