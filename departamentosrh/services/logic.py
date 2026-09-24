from django.db.models import Max, IntegerField
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError

from empresas.models import Empresas
from departamentosrh.models import DepartamentosRh


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def proximo_codigo_departamento(*, banco: str, db_alias: str, empresa: int, filial: int) -> int:
    banco_limpo = _digits_only(banco)
    qs = DepartamentosRh.objects
    if db_alias:
        qs = qs.using(db_alias)
    max_codi = (
        qs.filter(registro=banco_limpo, depa_empr=int(empresa), depa_fili=int(filial))
        .aggregate(maximo=Coalesce(Max("depa_codi", output_field=IntegerField()), 0))
        .get("maximo")
        or 0
    )
    return int(max_codi) + 1


class DepartamentosRhService:

    @staticmethod
    def salvar_form(form, banco, db_alias, depa_empr=None, depa_fili=None, operacao=None, **kwargs):
        instance = form.save(commit=False)
        banco_limpo = _digits_only(banco)
        instance.registro = banco_limpo
        if depa_empr is not None:
            instance.depa_empr = depa_empr
        if depa_fili is not None:
            instance.depa_fili = depa_fili

        import datetime
        usuario = kwargs.get("usuario") or kwargs.get("username") or ""
        try:
            usuario_str = str(usuario.username)[:30] if usuario and hasattr(usuario, "username") else str(usuario or "")[:30]
        except Exception:
            usuario_str = ""

        agora = datetime.datetime.now()

        empr_i = int(getattr(instance, "depa_empr") or 0)
        fili_i = int(getattr(instance, "depa_fili") or 0)
        codi_v = getattr(instance, "depa_codi", None)
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
                orig_empr = getattr(obj_orig, "depa_empr", None)
                orig_fili = getattr(obj_orig, "depa_fili", None)
                orig_codi = getattr(obj_orig, "depa_codi", None)
                if orig_reg and not instance.registro:
                    instance.registro = orig_reg
                e_tmp = int(orig_empr) if str(orig_empr or "").isdigit() else None
                if e_tmp and (not empr_i or empr_i == 0):
                    instance.depa_empr = e_tmp
                    empr_i = int(instance.depa_empr)
                f_tmp = int(orig_fili) if str(orig_fili or "").isdigit() else None
                if f_tmp and (not fili_i or fili_i == 0):
                    instance.depa_fili = f_tmp
                    fili_i = int(instance.depa_fili)
                c_tmp = int(orig_codi) if str(orig_codi or "").isdigit() else None
                if c_tmp and (not codi_i or codi_i is None):
                    instance.depa_codi = c_tmp
                    codi_i = int(instance.depa_codi)

        if operacao == "criar":
            if codi_i is None or codi_i <= 0:
                instance.depa_codi = proximo_codigo_departamento(
                    banco=banco_limpo,
                    db_alias=db_alias,
                    empresa=empr_i,
                    filial=fili_i,
                )
                codi_i = int(instance.depa_codi)
            qs_existente = DepartamentosRh.objects
            if db_alias:
                qs_existente = qs_existente.using(db_alias)
            duplicado = qs_existente.filter(
                registro=banco_limpo,
                depa_empr=empr_i,
                depa_fili=fili_i,
                depa_codi=codi_i,
            ).exists()
            if duplicado:
                raise ValidationError(
                    f"Já existe um Departamento cadastrado com o Código {codi_i} "
                    f"para a Empresa/Filial selecionada."
                )
            instance.depa_usuario_inc = usuario_str or None
            instance.depa_data_inc = agora
        else:
            instance.depa_usuario_alt = usuario_str or None
            instance.depa_data_alt = agora

        try:
            instance.save(using=db_alias, operacao=operacao)
        except TypeError:
            instance.save(using=db_alias)
        return instance

    @staticmethod
    def excluir(*, banco: str, depa_empr: int, depa_fili: int, depa_codi: int, db_alias: str = None):
        """Exclui departamento pela CHAVE PRIMÁRIA COMPOSTA completa, via SQL RAW.

        Garante que o DELETE use: registro + depa_empr + depa_fili + depa_codi
        (sem risco de apagar mais de um registro por limitação do Django com PK composta).
        """
        from django.db import connections

        banco_limpo = _digits_only(banco)
        alias = db_alias or "default"
        sql = (
            "DELETE FROM departamentosrh "
            "WHERE registro = %s "
            "  AND depa_empr = %s "
            "  AND depa_fili = %s "
            "  AND depa_codi = %s"
        )
        params = [
            str(banco_limpo),
            int(depa_empr),
            int(depa_fili),
            int(depa_codi),
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
        return getattr(filial, "empr_fili_descr", "") or getattr(filial, "empr_nome", "") or ""

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
    def listar_departamentos(*, banco: str, db_alias: str = None,
                             codigo_empresa: int = 1, codigo_filial: int = 1,
                             incluir_inativos: bool = True) -> list:
        banco_limpo = _digits_only(banco)
        empr = int(codigo_empresa or 1)
        fili = int(codigo_filial or 1)
        qs = DepartamentosRh.objects
        if db_alias:
            qs = qs.using(db_alias)
        filtros = {
            "registro": banco_limpo,
            "depa_empr": empr,
            "depa_fili": fili,
        }
        if not incluir_inativos:
            filtros["depa_inativo"] = False
        try:
            rows = list(
                qs.filter(**filtros)
                .order_by("depa_codi")
                .values_list(
                    "depa_codi", "depa_desc", "depa_apelido",
                    "depa_tipo_tomador", "depa_tipo_tomador_desc",
                    "depa_inativo",
                )
            )
        except Exception:
            from django.db import connections
            alias = db_alias or "default"
            try:
                with connections[alias].cursor() as cursor:
                    sql_inat = "" if incluir_inativos else " AND COALESCE(depa_inativo, FALSE) = FALSE"
                    cursor.execute(
                        "SELECT depa_codi, depa_desc, depa_apelido, "
                        "depa_tipo_tomador, depa_tipo_tomador_desc, COALESCE(depa_inativo, FALSE) "
                        "FROM departamentosrh "
                        f"WHERE registro=%s AND depa_empr=%s AND depa_fili=%s{sql_inat} "
                        "ORDER BY depa_codi",
                        [banco_limpo, empr, fili],
                    )
                    rows = cursor.fetchall() or []
            except Exception:
                rows = []
        saida = []
        seen = set()
        for cod, desc, apelido, t_tom, t_tom_desc, inativo in rows:
            cod_clean = str(int(cod or 0))
            if not cod_clean or cod_clean in seen:
                continue
            seen.add(cod_clean)
            desc_clean = str(desc or "").strip()
            label = desc_clean or f"Departamento #{cod_clean}"
            t_tom_int = None
            try:
                t_tom_int = int(t_tom) if str(t_tom or "").isdigit() else None
            except Exception:
                t_tom_int = None
            saida.append({
                "codi": int(cod_clean),
                "descricao": desc_clean,
                "apelido": str(apelido or "").strip(),
                "tipo_tomador": t_tom_int,
                "tipo_tomador_desc": str(t_tom_desc or "").strip(),
                "label": label,
                "inativo": bool(inativo),
            })
        return saida

    @staticmethod
    def choices_departamentos(*, banco: str, db_alias: str = None,
                             codigo_empresa: int = 1, codigo_filial: int = 1,
                             incluir_selecione: bool = True, valor_atual=None,
                             incluir_inativos: bool = True) -> list:
        lista = DepartamentosRhService.listar_departamentos(
            banco=banco,
            db_alias=db_alias,
            codigo_empresa=codigo_empresa,
            codigo_filial=codigo_filial,
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
                existe = False
                for chave, _ in choices:
                    try:
                        if int(chave) == val_int:
                            existe = True
                            break
                    except Exception:
                        pass
                if not existe and val_int > 0:
                    choices.append((val_int, f"{val_int} - Departamento #{val_int} (atual)"))
            except Exception:
                pass
        return choices
