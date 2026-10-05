from django.db.models import Max, IntegerField
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError

from empresas.models import Empresas
from prepara_recisoes.models import PreparaRescisoes


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def proximo_codigo_prepara_rescisao(*, banco: str, db_alias: str, empresa: int, filial: int) -> int:
    banco_limpo = _digits_only(banco)
    qs = PreparaRescisoes.objects
    if db_alias:
        qs = qs.using(db_alias)
    max_codi = (
        qs.filter(registro=banco_limpo, prep_empr=int(empresa), prep_fili=int(filial))
        .aggregate(maximo=Coalesce(Max("prep_codi", output_field=IntegerField()), 0))
        .get("maximo") or 0
    )
    return int(max_codi) + 1


class PreparaRescisoesService:

    @staticmethod
    def salvar_form(form, banco, db_alias, prep_empr=None, prep_fili=None, operacao=None, **kwargs):
        instance = form.save(commit=False)
        banco_limpo = _digits_only(banco)
        instance.registro = banco_limpo
        if prep_empr is not None:
            instance.prep_empr = prep_empr
        if prep_fili is not None:
            instance.prep_fili = prep_fili

        import datetime
        usuario = kwargs.get("usuario") or kwargs.get("username") or ""
        try:
            usuario_str = str(getattr(usuario, "username", ""))[:30]
            if not usuario_str:
                usuario_str = str(usuario or "")[:30]
        except Exception:
            usuario_str = ""

        today = datetime.date.today()

        empr_i = int(getattr(instance, "prep_empr") or 0)
        fili_i = int(getattr(instance, "prep_fili") or 0)
        codi_v = getattr(instance, "prep_codi", None)
        codi_i = int(codi_v) if str(codi_v or "").isdigit() else None

        if operacao not in ("criar", "editar"):
            try:
                modo_instancia = getattr(form.instance, "pk", None)
                operacao = "editar" if modo_instancia is not None else "criar"
            except Exception:
                operacao = "criar"

        if operacao == "editar":
            obj_orig = getattr(form, "instance", None)
            if obj_orig is not None:
                orig_reg = getattr(obj_orig, "registro", None)
                orig_empr = getattr(obj_orig, "prep_empr", None)
                orig_fili = getattr(obj_orig, "prep_fili", None)
                orig_codi = getattr(obj_orig, "prep_codi", None)
                if orig_reg and not instance.registro:
                    instance.registro = orig_reg
                e_tmp = int(orig_empr) if str(orig_empr or "").isdigit() else None
                if e_tmp and (not empr_i or empr_i == 0):
                    instance.prep_empr = e_tmp
                    empr_i = int(instance.prep_empr)
                f_tmp = int(orig_fili) if str(orig_fili or "").isdigit() else None
                if f_tmp and (not fili_i or fili_i == 0):
                    instance.prep_fili = f_tmp
                    fili_i = int(instance.prep_fili)
                c_tmp = int(orig_codi) if str(orig_codi or "").isdigit() else None
                if c_tmp and (not codi_i or codi_i is None):
                    instance.prep_codi = c_tmp
                    codi_i = int(instance.prep_codi)

        if operacao == "criar":
            if codi_i is None or codi_i <= 0:
                instance.prep_codi = proximo_codigo_prepara_rescisao(
                    banco=banco_limpo,
                    db_alias=db_alias,
                    empresa=empr_i,
                    filial=fili_i,
                )
                codi_i = int(instance.prep_codi)
            qs_existente = PreparaRescisoes.objects
            if db_alias:
                qs_existente = qs_existente.using(db_alias)
            duplicado = qs_existente.filter(
                registro=banco_limpo,
                prep_empr=empr_i,
                prep_fili=fili_i,
                prep_codi=codi_i,
            ).exists()
            if duplicado:
                raise ValidationError(
                    f"Já existe uma Preparação de Rescisão cadastrada com o Código {codi_i} "
                    "para a Empresa/Filial selecionada."
                )
            instance.prep_usuario_inc = usuario_str or None
            instance.prep_data_inc = today
        else:
            instance.prep_usuario_alt = usuario_str or None
            instance.prep_data_alt = today

        try:
            instance.save(using=db_alias, operacao=operacao)
        except TypeError:
            instance.save(using=db_alias)
        return instance

    @staticmethod
    def excluir(*, banco: str, prep_empr: int, prep_fili: int, prep_codi: int, db_alias: str = None):
        from django.db import connections

        banco_limpo = _digits_only(banco)
        alias = db_alias or "default"
        sql = (
            "DELETE FROM prepara_rescisoes "
            "WHERE registro = %s AND prep_empr = %s AND prep_fili = %s AND prep_codi = %s"
        )
        params = [
            str(banco_limpo),
            int(prep_empr),
            int(prep_fili),
            int(prep_codi),
        ]
        with connections[alias].cursor() as cur:
            cur.execute(sql, params)

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
            qs.filter(
                registro=_digits_only(banco),
                empr_empr=codigo_empresa,
                empr_fili=codigo_filial,
            )
            .first()
        )
        return (getattr(filial, "empr_fili_descr", "")
                or getattr(filial, "empr_nome", "")
                or "")

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
    def listar(*, banco: str, db_alias: str = None,
               codigo_empresa: int = 1, codigo_filial: int = 1,
               incluir_inativos: bool = True) -> list:
        banco_limpo = _digits_only(banco)
        empr = int(codigo_empresa or 1)
        fili = int(codigo_filial or 1)
        qs = PreparaRescisoes.objects
        if db_alias:
            qs = qs.using(db_alias)
        filtros = {"registro": banco_limpo, "prep_empr": empr, "prep_fili": fili}
        if not incluir_inativos:
            filtros["prep_inativo"] = False
        try:
            rows = list(
                qs.filter(**filtros)
                .order_by("prep_codi")
                .values_list(
                    "prep_codi", "prep_desc", "prep_descricao",
                    "prep_iniciativa_desc", "prep_aviso_previo_desc",
                    "prep_inativo", "prep_motivo_esocial_codi",
                    "prep_motivo_esocial_desc",
                )
            )
        except Exception:
            from django.db import connections
            alias = db_alias or "default"
            try:
                with connections[alias].cursor() as cur:
                    sql_inat = "" if incluir_inativos else " AND COALESCE(prep_inativo, FALSE) = FALSE"
                    cur.execute(
                        "SELECT prep_codi, prep_desc, prep_descricao, "
                        "prep_iniciativa_desc, prep_aviso_previo_desc, COALESCE(prep_inativo, FALSE), "
                        "prep_motivo_esocial_codi, prep_motivo_esocial_desc "
                        "FROM prepara_rescisoes "
                        f"WHERE registro=%s AND prep_empr=%s AND prep_fili=%s{sql_inat} "
                        "ORDER BY prep_codi",
                        [banco_limpo, empr, fili],
                    )
                    rows = cur.fetchall() or []
            except Exception:
                rows = []
        saida = []
        vistos = set()
        for cod, desc_tit, desc_comp, iniciativa, aviso, inativo, ms_cod, ms_desc in rows:
            cod_clean = str(int(cod or 0))
            if not cod_clean or cod_clean in vistos:
                continue
            vistos.add(cod_clean)
            desc_tit_clean = str(desc_tit or "").strip()
            desc_comp_clean = str(desc_comp or "").strip()
            label = desc_comp_clean or desc_tit_clean or f"Preparação de Rescisão #{cod_clean}"
            saida.append({
                "codi": int(cod_clean),
                "desc": desc_tit_clean,
                "descricao": desc_comp_clean,
                "iniciativa": str(iniciativa or "").strip(),
                "aviso_previo": str(aviso or "").strip(),
                "motivo_esocial_codi": str(ms_cod or "").strip(),
                "motivo_esocial_desc": str(ms_desc or "").strip(),
                "label": label,
                "inativo": bool(inativo),
            })
        return saida

    @staticmethod
    def choices(*, banco: str, db_alias: str = None,
                codigo_empresa: int = 1, codigo_filial: int = 1,
                incluir_selecione: bool = True, valor_atual=None,
                incluir_inativos: bool = True) -> list:
        lista = PreparaRescisoesService.listar(
            banco=banco, db_alias=db_alias,
            codigo_empresa=codigo_empresa, codigo_filial=codigo_filial,
            incluir_inativos=incluir_inativos,
        )
        choices = []
        if incluir_selecione:
            choices.append((None, "Selecione"))
        for item in lista:
            codi_int = int(item["codi"])
            rotulo = f"{item['codi']} - {item['label']}"
            if item.get("inativo"):
                rotulo = f"{rotulo} (Inativo)"
            choices.append((codi_int, rotulo))
        if valor_atual is not None:
            try:
                val_int = int(valor_atual)
                existe = any(int(ch) == val_int for ch, _ in choices if ch is not None)
                if not existe and val_int > 0:
                    choices.append((val_int, f"{val_int} - Preparação #{val_int} (atual)"))
            except Exception:
                pass
        return choices
