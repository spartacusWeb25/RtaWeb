from django.db.models import Max, IntegerField
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError

from empresas.models import Empresas
from cargos.models import Cargos


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def proximo_codigo_cargo(*, banco: str, db_alias: str, empresa: int, filial: int) -> int:
    banco_limpo = _digits_only(banco)
    qs = Cargos.objects
    if db_alias:
        qs = qs.using(db_alias)
    max_codi = (
        qs.filter(registro=banco_limpo, carg_empr=int(empresa), carg_fili=int(filial))
        .aggregate(maximo=Coalesce(Max("carg_codi", output_field=IntegerField()), 0))
        .get("maximo")
        or 0
    )
    return int(max_codi) + 1


class CargosService:

    @staticmethod
    def salvar_form(form, banco, db_alias, carg_empr=None, carg_fili=None, operacao=None, **kwargs):
        instance = form.save(commit=False)
        banco_limpo = _digits_only(banco)
        instance.registro = banco_limpo
        if carg_empr is not None:
            instance.carg_empr = carg_empr
        if carg_fili is not None:
            instance.carg_fili = carg_fili

        empr_i = int(getattr(instance, "carg_empr") or 0)
        fili_i = int(getattr(instance, "carg_fili") or 0)
        codi_v = getattr(instance, "carg_codi", None)
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
                orig_empr = getattr(obj_orig, "carg_empr", None)
                orig_fili = getattr(obj_orig, "carg_fili", None)
                orig_codi = getattr(obj_orig, "carg_codi", None)
                if orig_reg and not instance.registro:
                    instance.registro = orig_reg
                e_tmp = int(orig_empr) if str(orig_empr or "").isdigit() else None
                if e_tmp and (not empr_i or empr_i == 0):
                    instance.carg_empr = e_tmp
                    empr_i = int(instance.carg_empr)
                f_tmp = int(orig_fili) if str(orig_fili or "").isdigit() else None
                if f_tmp and (not fili_i or fili_i == 0):
                    instance.carg_fili = f_tmp
                    fili_i = int(instance.carg_fili)
                c_tmp = int(orig_codi) if str(orig_codi or "").isdigit() else None
                if c_tmp and (not codi_i or codi_i is None):
                    instance.carg_codi = c_tmp
                    codi_i = int(instance.carg_codi)

        if operacao == "criar":
            if codi_i is None or codi_i <= 0:
                instance.carg_codi = proximo_codigo_cargo(
                    banco=banco_limpo,
                    db_alias=db_alias,
                    empresa=empr_i,
                    filial=fili_i,
                )
                codi_i = int(instance.carg_codi)
            qs_existente = Cargos.objects
            if db_alias:
                qs_existente = qs_existente.using(db_alias)
            duplicado = qs_existente.filter(
                registro=banco_limpo,
                carg_empr=empr_i,
                carg_fili=fili_i,
                carg_codi=codi_i,
            ).exists()
            if duplicado:
                raise ValidationError(
                    f"Já existe um Cargo cadastrado com o Código {codi_i} "
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
    def listar_cbos(*, banco: str, db_alias: str = None):
        banco_limpo = _digits_only(banco)
        alias = db_alias or "default"
        itens = []

        def _clean_codi(codi):
            return _digits_only(codi)[:7] if codi is not None else ""

        def _clean_desc(desc):
            return (str(desc).strip() if desc else "") or ""

        def _print_log(msg):
            try:
                print(f"[CBO Service] {msg}")
            except Exception:
                pass

        # PRIORIDADE PARA CBOs REPETIDOS (mesmo cod, multiplas descricoes)
        # Retorna a DESCRICAO PRINCIPAL para cada familia (não os sinonimos)
        # peso MENOR = maior prioridade
        _PALAVRAS_PRIORIDADE_PRINCIPAL = [
            ("^soldador$", -100),        # DESCRICAO EXATA "Soldador" = PRIORIDADE MAXIMA (sempre 1a)
            ("soldador", -90),           # qualquer descricao com "soldador" no meio (ex: soldador autogeno, mecanico) = alta
            ("montador soldador", -80),  # montador soldador (vem DEPOIS do puro Soldador)
            ("operador de maquina de soldar", -70),
            ("^alimentador de linha de producao$", -100),   # Alimentador de linha de producao EXATO = principal
            ("alimentador de linha", -90),
            ("abastecedor", -80),
            ("^agente de transito$", -100),   # Agente de transito EXATO
            ("agente de transito", -90),
            ("^oficial general", -100),
            ("oficial da aeronautica", -90),
            ("oficial do exercito", -90),
            ("oficial da marinha", -90),
            ("^praca do", -90),
            ("^professor concursado$", -100),
        ]

        import re as _re_peso

        def _peso_descricao(desc: str) -> int:
            if not desc:
                return 9999
            d_norm = (
                desc.lower()
                .replace("á", "a").replace("â", "a").replace("ã", "a").replace("à", "a")
                .replace("é", "e").replace("ê", "e")
                .replace("í", "i")
                .replace("ó", "o").replace("ô", "o").replace("õ", "o")
                .replace("ú", "u").replace("ü", "u")
                .replace("ç", "c")
            )
            # Remove parenteses extras para match de regex: ex "(motorista de caminhao)"
            d_norm_strip = d_norm.strip().strip("()")
            for padrao, peso in _PALAVRAS_PRIORIDADE_PRINCIPAL:
                if padrao.startswith("^") or padrao.endswith("$"):
                    if _re_peso.match(padrao, d_norm_strip):
                        return peso
                else:
                    if padrao in d_norm:
                        return peso
            return 100 + len(desc)

        try:
            from django.db import connections
            with connections[alias].cursor() as cursor:
                # =====================================================================
                # FONTE ÚNICA E EXCLUSIVA: public.tab_cbo
                # (Usuario importou 10.185 CBOs oficiais do MTE)
                # =====================================================================
                cursor.execute(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                      AND table_name   = 'tab_cbo'
                    """,
                )
                cols_tab = {r[0] for r in cursor.fetchall()}
                col_codi = None
                col_desc = None
                for c in ["cbo_codi", "codigo", "cod", "c_cbo", "codi"]:
                    if c in cols_tab:
                        col_codi = c
                        break
                if col_codi is None:
                    for c in cols_tab:
                        if "codi" in c or "cod" in c or c.endswith("_cbo"):
                            col_codi = c
                            break
                for d in ["cbo_desc", "descricao", "desc_cbo", "nome", "titulo"]:
                    if d in cols_tab:
                        col_desc = d
                        break
                if col_desc is None:
                    for d in cols_tab:
                        if "desc" in d or "nome" in d:
                            col_desc = d
                            break
                if col_codi is None:
                    _print_log("ERRO: tabela public.tab_cbo nao tem coluna de codigo CBO!")
                    return []

                desc_expr = col_desc if col_desc else "NULL::varchar"
                sql = (
                    f"SELECT DISTINCT {col_codi} AS c, {desc_expr} AS d "
                    f"FROM public.tab_cbo "
                    f"WHERE {col_codi} IS NOT NULL "
                    f"  AND TRIM({col_codi}) <> ''"
                )
                cursor.execute(sql)
                todas_linhas_tab_cbo = cursor.fetchall()
                _print_log(f"Tabela public.tab_cbo: {len(todas_linhas_tab_cbo)} linhas lidas (FONTE OFICIAL E ÚNICA)")

                # ========= AGRUPA POR CODIGO CBO (prioriza descricao PRINCIPAL) =========
                cod_para_melhor = {}  # cod -> (peso, desc)
                todas_descricoes_por_cod = {}  # cod -> [(peso, desc)]

                for codi_raw, desc_raw in todas_linhas_tab_cbo:
                    cod_clean = _clean_codi(codi_raw)
                    desc_clean = _clean_desc(desc_raw)
                    if not cod_clean or not desc_clean:
                        continue
                    peso = _peso_descricao(desc_clean)

                    # guarda para ordenar depois todas as variacoes (sinonimos)
                    if cod_clean not in todas_descricoes_por_cod:
                        todas_descricoes_por_cod[cod_clean] = []
                    todas_descricoes_por_cod[cod_clean].append((peso, desc_clean))

                    # salva o MELHOR (menor peso = principal)
                    if cod_clean not in cod_para_melhor:
                        cod_para_melhor[cod_clean] = (peso, desc_clean)
                    else:
                        if peso < cod_para_melhor[cod_clean][0]:
                            cod_para_melhor[cod_clean] = (peso, desc_clean)

                _print_log(f"CBOs únicos em tab_cbo: {len(cod_para_melhor)} (de {len(todas_linhas_tab_cbo)} linhas com sinonimos)")

                # ========= MONTA A LISTA FINAL =========
                # REGRA:
                #  - 1 entrada POR CODIGO CBO (a descricao PRINCIPAL = menor peso)
                #  - MAS: mantem os sinonimos como entradas SEPARADAS TAMBEM para o datalist
                #    (usuario pode pesquisar "Operador de maquina de soldar" e encontrar 724315 tambem)
                #  - ORDENACAO: primeiro por ordem numerica crescente do cod;
                #    no mesmo cod: MELHOR (principal) primeiro, depois sinonimos por ordem alfabetica

                lista_bruta = []  # (peso_geral, cod_clean, ordem_interna, descricao)
                for cod_clean, lista_pesos in todas_descricoes_por_cod.items():
                    lista_pesos.sort(key=lambda x: (x[0], x[1]))
                    for idx, (peso_desc, desc_desc) in enumerate(lista_pesos):
                        lista_bruta.append((cod_clean, idx, desc_desc, peso_desc))

                # ordenacao final: (codigo numerico, ordem interna (principal primeiro))
                def _sort_key(item):
                    try:
                        num = int(item[0])
                    except Exception:
                        num = 999999999
                    return (num, item[1])

                lista_bruta.sort(key=_sort_key)

                itens = []
                for cod_clean, _idx, desc_desc, _peso in lista_bruta:
                    itens.append({
                        "codi": cod_clean,
                        "desc": desc_desc,
                    })

                _print_log(f"TOTAL FINAL DE CBOs (incluindo sinonimos) para o datalist: {len(itens)}")

        except Exception as e_geral:
            _print_log(f"Erro geral listar_cbos tab_cbo: {type(e_geral).__name__}: {e_geral}")
            import traceback
            _print_log(traceback.format_exc())
            itens = []
        return itens

    @staticmethod
    def listar_cargos(*, banco: str, db_alias: str = None,
                      codigo_empresa: int = 1, codigo_filial: int = 1,
                      incluir_inativos: bool = True) -> list:
        banco_limpo = _digits_only(banco)
        empr = int(codigo_empresa or 1)
        fili = int(codigo_filial or 1)
        qs = Cargos.objects
        if db_alias:
            qs = qs.using(db_alias)
        filtros = {
            "registro": banco_limpo,
            "carg_empr": empr,
            "carg_fili": fili,
        }
        if not incluir_inativos:
            filtros["carg_inativo"] = False
        try:
            rows = list(
                qs.filter(**filtros)
                .order_by("carg_codi")
                .values_list("carg_codi", "carg_descricao", "carg_cbo_codi", "carg_cbo_desc", "carg_inativo")
            )
        except Exception:
            from django.db import connections
            alias = db_alias or "default"
            try:
                with connections[alias].cursor() as cursor:
                    sql_inativo = "" if incluir_inativos else " AND COALESCE(carg_inativo, FALSE) = FALSE"
                    cursor.execute(
                        "SELECT carg_codi, carg_descricao, carg_cbo_codi, carg_cbo_desc, COALESCE(carg_inativo, FALSE) "
                        "FROM cargos "
                        f"WHERE registro=%s AND carg_empr=%s AND carg_fili=%s{sql_inativo} "
                        "ORDER BY carg_codi",
                        [banco_limpo, empr, fili],
                    )
                    rows = cursor.fetchall() or []
            except Exception:
                rows = []
        saida = []
        seen = set()
        for cod, desc, cbo_cod, cbo_desc, inativo in rows:
            cod_clean = str(int(cod or 0))
            if not cod_clean or cod_clean in seen:
                continue
            seen.add(cod_clean)
            desc_clean = str(desc or "").strip()
            label = desc_clean or f"Cargo #{cod_clean}"
            cbo_cod_clean = _digits_only(cbo_cod)[:7] if cbo_cod is not None else ""
            cbo_desc_clean = str(cbo_desc or "").strip()
            saida.append({
                "codi": int(cod_clean),
                "descricao": desc_clean,
                "label": label,
                "cbo_codi": cbo_cod_clean,
                "cbo_desc": cbo_desc_clean,
                "inativo": bool(inativo),
            })
        return saida

    @staticmethod
    def choices_cargos(*, banco: str, db_alias: str = None,
                       codigo_empresa: int = 1, codigo_filial: int = 1,
                       incluir_selecione: bool = True, valor_atual=None,
                       incluir_inativos: bool = True) -> list:
        lista = CargosService.listar_cargos(
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
                    choices.append((val_int, f"{val_int} - Cargo #{val_int} (atual)"))
            except Exception:
                pass
        return choices

    @staticmethod
    def choices_cbos(*, banco: str, db_alias: str = None,
                     incluir_selecione: bool = True, valor_atual=None) -> list:
        lista = CargosService.listar_cbos(banco=banco, db_alias=db_alias)
        choices = []
        if incluir_selecione:
            choices.append((None, "Selecione"))
        for item in lista:
            codi_clean = _digits_only(item.get("codi", ""))[:7]
            if not codi_clean:
                continue
            desc = str(item.get("desc") or "").strip() or f"CBO {codi_clean}"
            choices.append((codi_clean, f"{codi_clean} - {desc}"))
        if valor_atual is not None:
            try:
                val_clean = _digits_only(valor_atual)[:7]
                if val_clean:
                    existe = False
                    for chave, _ in choices:
                        if str(chave) == val_clean:
                            existe = True
                            break
                    if not existe:
                        choices.append((val_clean, f"{val_clean} - CBO {val_clean} (atual)"))
            except Exception:
                pass
        return choices
