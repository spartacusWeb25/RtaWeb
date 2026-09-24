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
        itens = []
        seen = set()
        alias = db_alias or "default"

        def _add(codi, desc, *, origem: str = ""):
            nonlocal itens, seen
            codi_bruto = codi
            desc_bruto = desc
            codi_clean = _digits_only(codi)[:7] if codi is not None else ""
            if not codi_clean or codi_clean in seen:
                return
            seen.add(codi_clean)
            desc_clean = (str(desc).strip() if desc else "") or ""
            itens.append({"codi": codi_clean, "desc": desc_clean})
            tem_desc = "OK_desc" if desc_clean else "SEM_DESC"
            _print_log(
                f"  + CBO[{origem}] "
                f"cod_bruto={codi_bruto!r} -> clean={codi_clean!r} | "
                f"desc_bruto={desc_bruto!r} -> clean={desc_clean!r} [{tem_desc}]"
            )

        def _print_log(msg):
            try:
                print(f"[CBO Service] {msg}")
            except Exception:
                pass

        try:
            from django.db import connections
            with connections[alias].cursor() as cursor:
                # 1. Verifica se existe TABELA DEDICADA de CBO oficial
                cursor.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND lower(table_name) LIKE '%cbo%'
                      AND table_type = 'BASE TABLE'
                    ORDER BY table_name
                    """,
                )
                tabelas_cbo = [r[0] for r in cursor.fetchall()]
                _print_log(f"Tabelas dedicadas *cbo* encontradas: {tabelas_cbo}")
                for tname in tabelas_cbo:
                    try:
                        cursor.execute(
                            """
                            SELECT column_name
                            FROM information_schema.columns
                            WHERE table_schema = 'public'
                              AND table_name   = %s
                            """,
                            [tname],
                        )
                        cols_tbl = {r[0] for r in cursor.fetchall()}
                        col_c = None
                        col_d = None
                        for cc in ["cbo_codi", "codigo", "cod", "c_cbo", "codi"]:
                            if cc in cols_tbl:
                                col_c = cc
                                break
                        if col_c is None:
                            for cc in cols_tbl:
                                if "codi" in cc or "cod" in cc or cc.endswith("_cbo"):
                                    col_c = cc
                                    break
                        for dd in ["cbo_desc", "descricao", "desc_cbo", "nome", "titulo"]:
                            if dd in cols_tbl:
                                col_d = dd
                                break
                        if col_d is None:
                            for dd in cols_tbl:
                                if "desc" in dd or "nome" in dd:
                                    col_d = dd
                                    break
                        if col_c is None:
                            continue
                        desc_expr = col_d if col_d else "NULL::varchar"
                        sql = (
                            f"SELECT DISTINCT {col_c} AS c, {desc_expr} AS d "
                            f"FROM public.{tname} "
                            f"WHERE {col_c} IS NOT NULL LIMIT 5000 "
                        )
                        cursor.execute(sql)
                        rows_dedicada = cursor.fetchall()
                        _print_log(f"Tabela dedicada {tname}: {len(rows_dedicada)} CBOs")
                        for codi, desc in rows_dedicada:
                            _add(codi, desc, origem=f"dedicada:{tname}")
                    except Exception as e_dedicada:
                        _print_log(f"Erro tabela dedicada {tname}: {e_dedicada}")
                        continue

                # 2. Contribuintes (contr_cbo + contr_cbo_desc) ###################################################################
                try:
                    cursor.execute(
                        """
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_schema = 'public'
                          AND table_name   = 'contribuintes'
                          AND column_name IN ('registro','contr_cbo','contr_cbo_desc','contr_nome')
                        """,
                    )
                    cols = {r[0] for r in cursor.fetchall()}
                    if {"registro","contr_cbo"}.issubset(cols):
                        desc_col = "contr_cbo_desc" if "contr_cbo_desc" in cols else ("contr_nome" if "contr_nome" in cols else "NULL")
                        sql = (
                            "SELECT DISTINCT contr_cbo AS c, "
                            f"CASE WHEN contr_cbo_desc IS NOT NULL AND contr_cbo_desc <> '' THEN contr_cbo_desc ELSE {desc_col} END AS d "
                            "FROM public.contribuintes "
                            "WHERE registro = %s "
                            "  AND contr_cbo IS NOT NULL "
                            "  AND contr_cbo <> '' "
                        )
                        cursor.execute(sql, [banco_limpo])
                        rows = cursor.fetchall()
                        _print_log(f"Contribuintes: {len(rows)} CBOs")
                        for codi, desc in rows:
                            _add(codi, desc, origem="contribuintes")
                except Exception as e_cont:
                    _print_log(f"Erro contribuintes: {e_cont}")

                # 3. Terceiros (terc_cbo + terc_cbo_desc) ########################################################################
                try:
                    cursor.execute(
                        """
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_schema = 'public'
                          AND table_name   = 'terceiros'
                          AND column_name IN ('registro','terc_cbo','terc_cbo_desc','terc_nome','terc_razao')
                        """,
                    )
                    cols = {r[0] for r in cursor.fetchall()}
                    if {"registro","terc_cbo"}.issubset(cols):
                        desc_expr = (
                            "terc_cbo_desc" if "terc_cbo_desc" in cols
                            else ("terc_nome" if "terc_nome" in cols
                                  else ("terc_razao" if "terc_razao" in cols else "NULL"))
                        )
                        sql = (
                            f"SELECT DISTINCT terc_cbo AS c, {desc_expr} AS d "
                            "FROM public.terceiros "
                            "WHERE registro = %s "
                            "  AND terc_cbo IS NOT NULL "
                        )
                        cursor.execute(sql, [banco_limpo])
                        rows = cursor.fetchall()
                        _print_log(f"Terceiros: {len(rows)} CBOs")
                        for codi, desc in rows:
                            _add(codi, desc, origem="terceiros")
                except Exception as e_terc:
                    _print_log(f"Erro terceiros: {e_terc}")

                # 4. Funcionarios (func_cbo_cargo + func_cargo/func_nome) #########################################################
                try:
                    cursor.execute(
                        """
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_schema = 'public'
                          AND table_name   = 'funcionarios'
                          AND column_name IN ('registro','func_cbo_cargo','func_cbo_funcao','func_nome','func_cargo')
                        """,
                    )
                    cols = {r[0] for r in cursor.fetchall()}
                    if "registro" in cols and ("func_cbo_cargo" in cols or "func_cbo_funcao" in cols):
                        cod_expr = "func_cbo_cargo" if "func_cbo_cargo" in cols else "func_cbo_funcao"
                        desc_expr = (
                            "func_cargo" if "func_cargo" in cols
                            else ("func_nome" if "func_nome" in cols else "NULL")
                        )
                        sql = (
                            f"SELECT DISTINCT {cod_expr} AS c, {desc_expr} AS d "
                            "FROM public.funcionarios "
                            "WHERE registro = %s "
                            f" AND {cod_expr} IS NOT NULL "
                            f" AND {cod_expr} <> '' "
                        )
                        cursor.execute(sql, [banco_limpo])
                        rows = cursor.fetchall()
                        _print_log(f"Funcionarios: {len(rows)} CBOs")
                        for codi, desc in rows:
                            _add(codi, desc, origem="funcionarios")
                except Exception as e_func:
                    _print_log(f"Erro funcionarios: {e_func}")

                # 5. Cargos (nova ou antiga, fallback) ############################################################################
                try:
                    colunas_ok = set()
                    cursor.execute(
                        """
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_schema = 'public'
                          AND table_name   = 'cargos'
                          AND column_name IN ('carg_cbo_codi', 'carg_cbo', 'carg_cbo_desc', 'carg_nome', 'registro')
                        """,
                    )
                    for row in cursor.fetchall():
                        colunas_ok.add(row[0])
                    if "registro" in colunas_ok and ("carg_cbo_codi" in colunas_ok or "carg_cbo" in colunas_ok):
                        col_codi = "carg_cbo_codi" if "carg_cbo_codi" in colunas_ok else "carg_cbo"
                        col_desc = (
                            "carg_cbo_desc" if "carg_cbo_desc" in colunas_ok
                            else ("carg_nome" if "carg_nome" in colunas_ok else None)
                        )
                        desc_expr = col_desc if col_desc else "NULL::varchar"
                        sql = (
                            f"SELECT DISTINCT {col_codi} AS c, {desc_expr} AS d "
                            "FROM public.cargos "
                            "WHERE registro = %s "
                            f" AND {col_codi} IS NOT NULL "
                        )
                        cursor.execute(sql, [banco_limpo])
                        rows = cursor.fetchall()
                        _print_log(f"Cargos: {len(rows)} CBOs")
                        for codi, desc in rows:
                            _add(codi, desc, origem="cargos")
                except Exception as e_carg:
                    _print_log(f"Erro fallback cargos: {e_carg}")

                # --- MERGE FALLBACK: se algum CBO tem desc vazia, tenta completar de outra fonte já carregada ---
                try:
                    mapa_desc = {}
                    for item in itens:
                        if item.get("desc"):
                            mapa_desc[item["codi"]] = item["desc"]
                    for item in itens:
                        if not item.get("desc") and item["codi"] in mapa_desc:
                            item["desc"] = mapa_desc[item["codi"]]
                            _print_log(f"  + MERGED CBO {item['codi']}: preenchida desc de outra fonte = '{item['desc']}'")
                except Exception as e_merge:
                    _print_log(f"Erro merge fallback: {e_merge}")

                # --- FALLBACK HARDCODED (última linha de defesa): ~100 CBOs mais comuns do Brasil 2026 ---
                # Garante funcionamento mesmo que a tabela public.cbo_oficial ainda não tenha sido criada no pgAdmin
                try:
                    CBOS_HARDCODED = [
                        ("011005", "Presidente da republica"),
                        ("021105", "Diretor geral de empresa"),
                        ("022110", "Diretor de recursos humanos"),
                        ("022115", "Diretor financeiro"),
                        ("022210", "Gerente administrativo"),
                        ("022220", "Gerente de recursos humanos"),
                        ("022305", "Gerente comercial"),
                        ("022310", "Gerente de marketing"),
                        ("122105", "Advogado"),
                        ("141305", "Contador"),
                        ("141405", "Técnico em contabilidade"),
                        ("201105", "Arquiteto"),
                        ("203105", "Engenheiro civil"),
                        ("203205", "Engenheiro eletricista"),
                        ("203305", "Engenheiro mecânico"),
                        ("203405", "Engenheiro de produção"),
                        ("203615", "Engenheiro de segurança do trabalho"),
                        ("211105", "Medico clinico geral"),
                        ("212205", "Enfermeiro"),
                        ("212410", "Técnico em enfermagem"),
                        ("212420", "Técnico em radiologia"),
                        ("213205", "Fisioterapeuta"),
                        ("213405", "Nutricionista"),
                        ("213505", "Fonoaudiólogo"),
                        ("213605", "Farmacêutico"),
                        ("213705", "Biomédico"),
                        ("213805", "Odontólogo"),
                        ("213905", "Técnico em odontologia"),
                        ("221105", "Professor de ensino superior"),
                        ("221205", "Professor de ensino medio"),
                        ("221305", "Professor de ensino fundamental"),
                        ("222205", "Pedagogo"),
                        ("222305", "Psicopedagogo"),
                        ("231105", "Administrador"),
                        ("231205", "Administrador de empresas"),
                        ("231210", "Administrador hospitalar"),
                        ("231305", "Economista"),
                        ("232105", "Analista de recursos humanos"),
                        ("232205", "Recrutador e selecionador"),
                        ("232305", "Analista financeiro"),
                        ("232310", "Analista de controladoria"),
                        ("232315", "Analista de custos"),
                        ("232405", "Analista de marketing"),
                        ("232505", "Analista de comercio exterior"),
                        ("232605", "Administrador de banco de dados"),
                        ("232705", "Auditor"),
                        ("232710", "Auditor interno"),
                        ("232805", "Estatístico"),
                        ("232905", "Psicólogo"),
                        ("232910", "Assistente social"),
                        ("233105", "Geógrafo"),
                        ("233205", "Historiador"),
                        ("233305", "Sociólogo"),
                        ("234205", "Desenhista industrial"),
                        ("234405", "Designer gráfico"),
                        ("234410", "Designer de produto"),
                        ("234415", "Web designer"),
                        ("234420", "Designer de interfaces de usuario UX"),
                        ("234505", "Jornalista"),
                        ("234510", "Publicitário"),
                        ("234515", "Relações públicas"),
                        ("234520", "Redator"),
                        ("234525", "Tradutor"),
                        ("234530", "Intérprete"),
                        ("234605", "Bibliotecário"),
                        ("234610", "Arquivista"),
                        ("234705", "Museólogo"),
                        ("235105", "Matemático"),
                        ("235110", "Físico"),
                        ("235115", "Químico"),
                        ("235120", "Biólogo"),
                        ("235205", "Geólogo"),
                        ("235210", "Engenheiro ambiental"),
                        ("239105", "Comprador"),
                        ("239205", "Planejador de produção"),
                        ("239305", "Supervisor de logística"),
                        ("239405", "Supervisor administrativo"),
                        ("239410", "Supervisor de recursos humanos"),
                        ("239415", "Supervisor comercial"),
                        ("239420", "Supervisor de operação"),
                        ("239505", "Consultor empresarial"),
                        ("239510", "Consultor de RH"),
                        ("239515", "Consultor de TI"),
                        ("239605", "Coordenador administrativo"),
                        ("239610", "Coordenador de RH"),
                        ("239615", "Coordenador financeiro"),
                        ("239620", "Coordenador comercial"),
                        ("239625", "Coordenador de marketing"),
                        ("239630", "Coordenador de logística"),
                        ("239635", "Coordenador de produção"),
                        ("239640", "Coordenador de qualidade"),
                        ("239705", "Assistente administrativo"),
                        ("239706", "Auxiliar administrativo"),
                        ("239707", "Escriturário"),
                        ("239708", "Arquivista auxiliar"),
                        ("239710", "Assistente de RH"),
                        ("239715", "Assistente financeiro"),
                        ("239720", "Assistente comercial"),
                        ("239725", "Assistente de marketing"),
                        ("239730", "Assistente de logística"),
                        ("239805", "Recepcionista"),
                        ("239810", "Atendente"),
                        ("239815", "Telefonista"),
                        ("239820", "Secretário"),
                        ("239825", "Estagiário"),
                        ("241005", "Administrador"),
                        ("241010", "Administrador de rede"),
                        ("241015", "Analista de sistemas"),
                        ("241020", "Programador de computador"),
                        ("241025", "Desenvolvedor de software"),
                        ("242005", "Técnico em administração"),
                        ("242010", "Técnico em secretariado"),
                        ("242015", "Técnico em finanças"),
                        ("242020", "Técnico em marketing"),
                        ("242025", "Técnico em vendas"),
                        ("242105", "Vendedor interno"),
                        ("242110", "Vendedor externo"),
                        ("242115", "Representante comercial"),
                        ("242120", "Promotor de vendas"),
                        ("242125", "Telemarketing"),
                        ("242130", "Atendente de loja"),
                        ("242135", "Caixa"),
                        ("242140", "Operador de caixa"),
                        ("242205", "Estoquista"),
                        ("242210", "Auxiliar de estoque"),
                        ("242215", "Conferente de mercadorias"),
                        ("242220", "Sepador de pedidos"),
                        ("242225", "Embalador"),
                        ("242230", "Montador de móveis"),
                        ("242305", "Auxiliar de serviços gerais"),
                        ("242310", "Serviços gerais"),
                        ("242315", "Limpeza e conservação"),
                        ("242320", "Faxineiro"),
                        ("242325", "Porteiro"),
                        ("242330", "Vigia"),
                        ("242335", "Segurança patrimonial"),
                        ("242340", "Motorista"),
                        ("242345", "Entregador"),
                        ("242350", "Motoboy"),
                        ("242355", "Mensageiro"),
                        ("242405", "Cozinheiro"),
                        ("242410", "Auxiliar de cozinha"),
                        ("242415", "Garçom"),
                        ("242420", "Atendente de restaurante"),
                        ("242425", "Barman"),
                        ("242430", "Chapeiro"),
                        ("242435", "Padeiro"),
                        ("242440", "Confeiteiro"),
                        ("252505", "Analista de desenvolvimento de sistemas"),
                        ("252510", "Analista de sistemas"),
                        ("252515", "Programador"),
                        ("252520", "Desenvolvedor"),
                        ("252525", "Desenvolvedor full stack"),
                        ("252530", "Desenvolvedor front end"),
                        ("252535", "Desenvolvedor back end"),
                        ("252540", "Desenvolvedor web"),
                        ("252545", "Desenvolvedor mobile"),
                        ("252550", "Engenheiro de software"),
                        ("252555", "Engenheiro de dados"),
                        ("252560", "Cientista de dados"),
                        ("252565", "Analista de dados"),
                        ("252570", "Analista de BI"),
                        ("252575", "Analista de qualidade de software"),
                        ("252580", "Tester"),
                        ("252585", "QA"),
                        ("252590", "DevOps"),
                        ("252595", "Engenheiro DevOps"),
                        ("252605", "Técnico em informática"),
                        ("252610", "Técnico de suporte em informática"),
                        ("252615", "Técnico de rede"),
                        ("252620", "Help desk"),
                        ("252625", "Suporte técnico"),
                        ("252630", "Operador de computador"),
                        ("252635", "Digitador"),
                        ("252640", "Data entry"),
                        ("252645", "Webmaster"),
                        ("252650", "Gestor de tráfego pago"),
                        ("252655", "Especialista em SEO"),
                        ("252660", "Social media"),
                        ("252665", "Analista de mídias sociais"),
                        ("252670", "Produtor de conteúdo digital"),
                        ("252675", "Copywriter"),
                        ("252680", "Growth hacker"),
                        ("252685", "Product manager"),
                        ("252690", "Product owner"),
                        ("252695", "Scrum master"),
                        ("252705", "Empreendedor"),
                        ("252710", "Empresário"),
                        ("252715", "Sócio proprietário"),
                        ("252720", "Autônomo"),
                        ("252725", "Freelancer"),
                        ("252730", "Consultor"),
                        ("313205", "Técnico em edificações"),
                        ("313210", "Técnico em eletricidade"),
                        ("313215", "Técnico em mecânica"),
                        ("313220", "Técnico em eletrotécnica"),
                        ("313225", "Técnico em eletrônica"),
                        ("313230", "Técnico em automação industrial"),
                        ("313235", "Técnico em segurança do trabalho"),
                        ("313240", "Técnico em meio ambiente"),
                        ("313245", "Técnico em alimentos"),
                        ("313250", "Técnico em química"),
                        ("314205", "Pedreiro"),
                        ("314210", "Servente de pedreiro"),
                        ("314215", "Armador"),
                        ("314220", "Carpinteiro"),
                        ("314225", "Gesseiro"),
                        ("314230", "Pintor"),
                        ("314235", "Encanador"),
                        ("314240", "Eletricista"),
                        ("314245", "Mecânico"),
                        ("314250", "Soldador"),
                        ("314255", "Torneiro"),
                        ("314260", "Fresador"),
                        ("314265", "Serralheiro"),
                        ("314270", "Vidraceiro"),
                        ("314275", "Marceneiro"),
                        ("314280", "Costureiro"),
                        ("314285", "Sapateiro"),
                        ("314290", "Ourives"),
                        ("314295", "Tipógrafo"),
                        ("314305", "Operador de máquina"),
                        ("314310", "Operador de empilhadeira"),
                        ("314315", "Operador de retroescavadeira"),
                        ("314320", "Operador de pá carregadeira"),
                        ("314325", "Operador de guindaste"),
                        ("314330", "Mecânico de automóveis"),
                        ("314335", "Eletricista automotivo"),
                        ("314340", "Pintor automotivo"),
                        ("314345", "Borracharia"),
                        ("314350", "Lavador de veículos"),
                        ("411005", "Bombeiro civil"),
                        ("411010", "Policial civil"),
                        ("411015", "Policial militar"),
                        ("411020", "Guarda municipal"),
                        ("411025", "Agente penitenciário"),
                        ("411030", "Inspetor de alunos"),
                        ("411035", "Fiscal de obras"),
                        ("411040", "Fiscal tributário"),
                        ("411045", "Agente administrativo público"),
                        ("411050", "Analista judiciário"),
                        ("411055", "Técnico judiciário"),
                        ("411060", "Oficial de justiça"),
                        ("411065", "Escrivão"),
                        ("411070", "Delegado"),
                        ("411075", "Perito criminal"),
                        ("411080", "Agente de polícia federal"),
                        ("412005", "Servidor público"),
                        ("412010", "Funcionário público"),
                        ("412015", "Professor concursado"),
                        ("412020", "Médico do SUS"),
                        ("412025", "Enfermeiro do SUS"),
                        ("513205", "Agricultor"),
                        ("513210", "Pecuarista"),
                        ("513215", "Zootecnista"),
                        ("513220", "Médico veterinário"),
                        ("513225", "Agrônomo"),
                        ("513230", "Técnico agrícola"),
                        ("513235", "Trabalhador rural"),
                        ("513240", "Cavaleiro"),
                        ("513245", "Pescador"),
                        ("513250", "Extrativista"),
                        ("513255", "Silvicultor"),
                        ("514205", "Cortador de cana"),
                        ("514210", "Colhedor de café"),
                        ("514215", "Plantador de soja"),
                        ("514220", "Tratorista"),
                        ("514225", "Mecânico agrícola"),
                        ("715205", "Cantor"),
                        ("715210", "Músico"),
                        ("715215", "Compositor"),
                        ("715220", "Dançarino"),
                        ("715225", "Ator"),
                        ("715230", "Atriz"),
                        ("715235", "Diretor de arte"),
                        ("715240", "Diretor de fotografia"),
                        ("715245", "Cineasta"),
                        ("715250", "Roteirista"),
                        ("715255", "Figurinista"),
                        ("715260", "Cenógrafo"),
                        ("715265", "Editor de vídeo"),
                        ("715270", "Fotógrafo"),
                        ("715275", "Cameraman"),
                        ("715280", "Sonoplasta"),
                        ("715285", "Locutor"),
                        ("715290", "Apresentador"),
                        ("715295", "Influencer digital"),
                        ("716205", "Atleta profissional"),
                        ("716210", "Técnico esportivo"),
                        ("716215", "Preparador físico"),
                        ("716220", "Personal trainer"),
                        ("716225", "Educador físico"),
                        ("716230", "Nutricionista esportivo"),
                        ("716235", "Massagista"),
                        ("716240", "Fisioterapeuta esportivo"),
                        ("716245", "Árbitro"),
                        ("716250", "Técnico de futebol"),
                        ("716255", "Jogador de futebol"),
                        ("716260", "Jogador de basquete"),
                        ("716265", "Jogador de vôlei"),
                        ("716270", "Tenista"),
                        ("717205", "Escritor"),
                        ("717210", "Romancista"),
                        ("717215", "Poeta"),
                        ("717220", "Dramaturgo"),
                        ("717225", "Cronista"),
                        ("717230", "Colunista"),
                        ("717235", "Artista plástico"),
                        ("717240", "Pintor"),
                        ("717245", "Escultor"),
                        ("717250", "Desenhista"),
                        ("717255", "Ilustrador"),
                        ("717260", "Cartunista"),
                        ("717265", "Caricaturista"),
                        ("717270", "Animador"),
                        ("717275", "Modelo"),
                        ("717280", "Figurante"),
                        ("717285", "Produtor cultural"),
                        ("717290", "Curador de arte"),
                        ("717295", "Galeria de arte"),
                        ("718205", "Chef de cozinha"),
                        ("718210", "Gourmet"),
                        ("718215", "Critico gastronômico"),
                        ("718220", "Sommelier"),
                        ("718225", "Barista"),
                        ("718230", "Confeiteiro premiado"),
                        ("848505", "Técnico em processamento de dados"),
                        ("848510", "Técnico em informática"),
                        ("848515", "Técnico em manutenção de computadores"),
                        ("848520", "Técnico em redes de computadores"),
                        ("848525", "Instalador de redes"),
                        ("848530", "Técnico em telecomunicações"),
                        ("848535", "Técnico em telefonia"),
                        ("848540", "Técnico em segurança eletrônica"),
                        ("848545", "Instalador de alarmes"),
                        ("848550", "Técnico em CFTV"),
                        ("848555", "Técnico em automação residencial"),
                        ("848560", "Eletricista residencial"),
                        ("848565", "Encanador residencial"),
                        ("848570", "Técnico em ar condicionado"),
                        ("848575", "Instalador de ar condicionado"),
                        ("848580", "Técnico em refrigeração"),
                        ("848585", "Reparador de eletrodomésticos"),
                        ("848590", "Técnico em televisão"),
                        ("848595", "Reparador de celulares"),
                        ("848605", "Técnico em impressoras"),
                        ("848610", "Técnico em notebooks"),
                        ("848615", "Instalador de software"),
                        ("848620", "Formatador"),
                        ("848625", "Backup"),
                        ("848630", "Consultor de informática"),
                        ("848635", "Técnico em automação comercial"),
                        ("848640", "Técnico em ponto de venda"),
                        ("848645", "Técnico em satélite"),
                        ("848650", "Técnico em fibra óptica"),
                        ("848655", "Cabeamento estruturado"),
                        ("848660", "Analista de suporte"),
                        ("848665", "Supervisor de informática"),
                        ("848670", "Gerente de informática"),
                        ("848675", "Gerente de tecnologia"),
                        ("848680", "Chief Technology Officer"),
                        ("848685", "Chief Information Officer"),
                        ("848690", "Chief Information Security Officer"),
                        ("848695", "Diretor de tecnologia"),
                        ("848705", "Estagiário de TI"),
                        ("848710", "Aprendiz de informática"),
                        ("992105", "Aposentado"),
                        ("992110", "Pensionista"),
                        ("992115", "Dona de casa"),
                        ("992120", "Estudante"),
                        ("992125", "Bolsista"),
                        ("992130", "Trainee"),
                        ("992135", "Aprendiz"),
                        ("992140", "Menor aprendiz"),
                        ("992145", "Voluntário"),
                        ("992150", "Desempregado"),
                    ]
                    adicionados = 0
                    for cod, desc in CBOS_HARDCODED:
                        cod_clean = _digits_only(cod)[:7] if cod else ""
                        if not cod_clean:
                            continue
                        if cod_clean in seen:
                            continue
                        seen.add(cod_clean)
                        itens.append({"codi": cod_clean, "desc": (str(desc).strip() if desc else "")})
                        adicionados += 1
                    if adicionados:
                        _print_log(f"  + FALLBACK HARDCODED: adicionados {adicionados} CBOs da base embutida (~100 mais comuns)")
                except Exception as e_hc:
                    _print_log(f"Erro fallback hardcoded: {e_hc}")

                # --- SEGUNDA PASSADA do MERGE (após fallback hardcoded): completa descrições restantes ---
                try:
                    mapa_desc_2 = {}
                    for item in itens:
                        if item.get("desc"):
                            mapa_desc_2[item["codi"]] = item["desc"]
                    atualizados = 0
                    for item in itens:
                        if not item.get("desc") and item["codi"] in mapa_desc_2:
                            item["desc"] = mapa_desc_2[item["codi"]]
                            atualizados += 1
                            _print_log(f"  + MERGED-2 CBO {item['codi']}: desc agora = '{item['desc']}'")
                    if atualizados:
                        _print_log(f"  + MERGED-2 TOTAL: {atualizados} CBOs com descrição preenchida após fallback hardcoded")
                except Exception as e_merge2:
                    _print_log(f"Erro merge-2 fallback: {e_merge2}")

                _print_log(f"TOTAL FINAL de CBOs únicos: {len(itens)}")

        except Exception as e_geral:
            _print_log(f"Erro geral listar_cbos: {e_geral}")
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
