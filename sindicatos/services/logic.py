from django.db.models import Max, IntegerField
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError
from empresas.models import Empresas
from sindicatos.models import Sindicatos


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def proximo_codigo_sindicato(*, banco: str, db_alias: str, empresa: int, filial: int) -> int:
    banco_limpo = _digits_only(banco)
    qs = Sindicatos.objects
    if db_alias:
        qs = qs.using(db_alias)
    max_codi = (
        qs.filter(registro=banco_limpo, sind_empr=int(empresa), sind_fili=int(filial))
        .aggregate(maximo=Coalesce(Max("sind_codi", output_field=IntegerField()), 0))
        .get("maximo")
        or 0
    )
    return int(max_codi) + 1


class SindicatoTrabalhadoresService:

    @staticmethod
    def salvar_form(form, banco, db_alias, sind_empr=None, sind_fili=None, operacao=None, **kwargs):
        instance = form.save(commit=False)
        banco_limpo = _digits_only(banco)
        instance.registro = banco_limpo
        if sind_empr is not None:
            instance.sind_empr = sind_empr
        if sind_fili is not None:
            instance.sind_fili = sind_fili

        empr_i = int(getattr(instance, "sind_empr") or 0)
        fili_i = int(getattr(instance, "sind_fili") or 0)
        codi_v = getattr(instance, "sind_codi", None)
        codi_i = int(codi_v) if str(codi_v or "").isdigit() else None

        if operacao not in ("criar", "editar"):
            try:
                modo_instancia = getattr(form.instance, "pk", None)
                operacao = "editar" if modo_instancia is not None else "criar"
            except Exception:
                operacao = "criar"

        if operacao == "criar":
            if codi_i is None or codi_i <= 0:
                instance.sind_codi = proximo_codigo_sindicato(
                    banco=banco_limpo,
                    db_alias=db_alias,
                    empresa=empr_i,
                    filial=fili_i,
                )
                codi_i = int(instance.sind_codi)
            qs_existente = Sindicatos.objects
            if db_alias:
                qs_existente = qs_existente.using(db_alias)
            duplicado = qs_existente.filter(
                registro=banco_limpo,
                sind_empr=empr_i,
                sind_fili=fili_i,
                sind_codi=codi_i,
            ).exists()
            if duplicado:
                raise ValidationError(
                    f"Já existe um Sindicato Trabalhador cadastrado com o Código {codi_i} "
                    f"para a Empresa/Filial selecionada."
                )

        try:
            instance.save(using=db_alias, operacao=operacao)
        except TypeError:
            instance.save(using=db_alias)
        return instance

    @staticmethod
    def excluir(instance, db_alias):
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
            qs.filter(
                registro=_digits_only(banco),
                empr_empr=codigo_empresa,
                empr_fili=codigo_filial,
            )
            .first()
        )
        return getattr(filial, "empr_fili_descr", "") or getattr(filial, "empr_nome", "") or ""

    @staticmethod
    def listar_sindicatos(*, banco: str, db_alias: str = None,
                          codigo_empresa: int = 1, codigo_filial: int = 1,
                          incluir_inativos: bool = True) -> list:
        banco_limpo = _digits_only(banco)
        empr = int(codigo_empresa or 1)
        fili = int(codigo_filial or 1)
        qs = Sindicatos.objects
        if db_alias:
            qs = qs.using(db_alias)
        filtros = {
            "registro": banco_limpo,
            "sind_empr": empr,
            "sind_fili": fili,
        }
        try:
            rows = list(
                qs.filter(**filtros)
                .order_by("sind_codi")
                .values_list("sind_codi", "sind_nome", "sind_apelido")
            )
        except Exception:
            from django.db import connections
            alias = db_alias or "default"
            try:
                with connections[alias].cursor() as cursor:
                    cursor.execute(
                        "SELECT sind_codi, sind_nome, sind_apelido "
                        "FROM sindicatos "
                        "WHERE registro=%s AND sind_empr=%s AND sind_fili=%s "
                        "ORDER BY sind_codi",
                        [banco_limpo, empr, fili],
                    )
                    rows = cursor.fetchall() or []
            except Exception:
                rows = []
        saida = []
        seen = set()
        for cod, nome, apelido in rows:
            cod_clean = str(int(cod or 0))
            if not cod_clean or cod_clean in seen:
                continue
            seen.add(cod_clean)
            nome_clean = str(nome or "").strip()
            apelido_clean = str(apelido or "").strip()
            if not nome_clean and apelido_clean:
                nome_clean = apelido_clean
            label = nome_clean or f"Sindicato #{cod_clean}"
            saida.append({"codi": int(cod_clean), "nome": nome_clean,
                          "apelido": apelido_clean, "label": label})
        return saida

    @staticmethod
    def choices_sindicatos(*, banco: str, db_alias: str = None,
                           codigo_empresa: int = 1, codigo_filial: int = 1,
                           incluir_selecione: bool = True, valor_atual=None) -> list:
        lista = SindicatoTrabalhadoresService.listar_sindicatos(
            banco=banco,
            db_alias=db_alias,
            codigo_empresa=codigo_empresa,
            codigo_filial=codigo_filial,
        )
        choices = []
        if incluir_selecione:
            sel_val = None
            choices.append((sel_val, "Selecione"))
        for item in lista:
            codi_int = int(item["codi"])
            choices.append((codi_int, f"{item['codi']} - {item['label']}"))
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
                    desc = f"Sindicato #{val_int} (atual)"
                    choices.append((val_int, desc))
            except Exception:
                pass
        return choices
