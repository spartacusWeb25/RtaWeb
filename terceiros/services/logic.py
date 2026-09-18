from django.core.exceptions import ValidationError
from django.db.models import Max, IntegerField
from django.db.models.functions import Coalesce
from empresas.models import Empresas
from terceiros.models import Terceiros


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def proximo_codigo_terceiro(*, banco: str, db_alias: str, empresa: int, filial: int) -> int:
    banco_limpo = _digits_only(banco)
    qs = Terceiros.objects
    if db_alias:
        qs = qs.using(db_alias)
    max_codi = (
        qs.filter(registro=banco_limpo, terc_empr=int(empresa), terc_fili=int(filial))
        .aggregate(maximo=Coalesce(Max("terc_codi", output_field=IntegerField()), 0))
        .get("maximo")
        or 0
    )
    return int(max_codi) + 1


class TerceirosService:

    @staticmethod
    def salvar_form(form, banco, db_alias, terc_empr=None, terc_fili=None, operacao=None, **kwargs):
        instance = form.save(commit=False)
        banco_limpo = _digits_only(banco)
        instance.registro = banco_limpo
        if terc_empr is not None:
            instance.terc_empr = terc_empr
        if terc_fili is not None:
            instance.terc_fili = terc_fili

        empr_i = int(getattr(instance, "terc_empr") or 0)
        fili_i = int(getattr(instance, "terc_fili") or 0)
        codi_v = getattr(instance, "terc_codi", None)
        codi_i = int(codi_v) if str(codi_v or "").isdigit() else None

        # --- DETECCAO MODO OPERACAO:
        #     "criar" -> Novo Terceiro (CreateView)
        #     "editar" -> Editar Terceiro (UpdateView)
        #     Se nao informado: inferir por heuristica antiga (mas NAO confiaveis)
        if operacao not in ("criar", "editar"):
            try:
                modo_instancia = getattr(form.instance, "pk", None)
                operacao = "editar" if modo_instancia is not None else "criar"
            except Exception:
                operacao = "criar"

        # ==========================================================
        # MODO CRIAR: 2 CAMADAS DE BLOQUEIO CONTRA DUPLICADA + SOBRESCRITA
        # ==========================================================
        if operacao == "criar":
            # --- CAMADA 1: se codigo nao informado, proximo automatico ---
            if codi_i is None or codi_i <= 0:
                instance.terc_codi = proximo_codigo_terceiro(
                    banco=banco_limpo,
                    db_alias=db_alias,
                    empresa=empr_i,
                    filial=fili_i,
                )
                codi_i = int(instance.terc_codi)
            # --- CAMADA 2: BLOQUEIO FATAL se usuário tentou gravar CÓDIGO JÁ EXISTENTE
            #     MESMO QUE MODEL.SAVE() FOSSE FAZER UPDATE ERRADO,
            #     AQUI A GENTE NAO DEIXA NEM CHEGAR LA ---
            qs_existente = Terceiros.objects
            if db_alias:
                qs_existente = qs_existente.using(db_alias)
            duplicado = qs_existente.filter(
                registro=banco_limpo,
                terc_empr=empr_i,
                terc_fili=fili_i,
                terc_codi=codi_i,
            ).exists()
            if duplicado:
                raise ValidationError(
                    f"Já existe um Terceiro cadastrado com o Código {codi_i} "
                    f"para a Empresa/Filial selecionada. "
                    f"Utilize outro código ou deixe o campo Código vazio para "
                    f"gerar automaticamente (próximo disponível: "
                    f"{proximo_codigo_terceiro(banco=banco_limpo, db_alias=db_alias, empresa=empr_i, filial=fili_i)})."
                )

        # --- ULTIMA CAMADA (segurança extra): PASSAR EXPLICITAMENTE o PARAMETRO
        #     `operacao` no save() para o model.save() SABER se deve INSERT ou UPDATE,
        #     sem confiar em instance.pk (estragado por primary_key=True em registro).
        try:
            instance.save(using=db_alias, operacao=operacao)
        except TypeError:
            instance.save(using=db_alias)
        return instance

    @staticmethod
    def excluir_terceiro(instance, db_alias):
        instance.delete(using=db_alias)

    @staticmethod
    def obter_nome_empresa(*, banco: str, db_alias: str = None, codigo_empresa=None) -> str:
        if not codigo_empresa:
            return ""

        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        empresa = (
            qs.filter(registro=_digits_only(banco), empr_empr=codigo_empresa)
            .order_by("empr_fili", "empr_nome")
            .first()
        )
        return getattr(empresa, "empr_nome", "") or ""

    @staticmethod
    def obter_nome_filial(*, banco: str, db_alias: str = None, codigo_empresa=None, codigo_filial=None) -> str:
        if not codigo_empresa or not codigo_filial:
            return ""

        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        filial = (
            qs.filter(registro=_digits_only(banco), empr_empr=codigo_empresa, empr_fili=codigo_filial)
            .order_by("empr_fili")
            .first()
        )
        descricao = getattr(filial, "empr_fant", "") or getattr(filial, "empr_nome", "") or ""
        if not descricao and codigo_filial == 1:
            return ""
        if not descricao:
            return f"Filial {codigo_filial} - Matriz" if codigo_filial == 1 else f"Filial {codigo_filial}"
        return f"Filial {codigo_filial} - {descricao}"

    @staticmethod
    def obter_empresa_padrao(*, banco: str, db_alias: str = None):
        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)

        return (
            qs.filter(registro=_digits_only(banco))
            .order_by("empr_empr", "empr_fili", "empr_nome")
            .first()
        )

    @staticmethod
    def obter_filial_padrao(*, banco: str, db_alias: str = None):
        return TerceirosService.obter_empresa_padrao(banco=banco, db_alias=db_alias)
