from decimal import Decimal, ROUND_HALF_UP
from django.db import connections


D0 = Decimal("0.00")


def valores(value):
    if value is None:
        return D0
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class FolhaMensal:
    """
    Service de leitura, conferência e consolidação da folha mensal.

    Regra de ouro:
    - Não recalcula oficialmente a folha.
    - Lê o legado em folhamensal.
    - Usa eventos para classificar incidências.
    - Usa tabelainss/tabelairrf para conferência tributária.
    """

    @staticmethod
    def listar_lancamentos(*, db_alias, registro, empresa, referencia, filial=None, funcionario=None, nome=None):
        sql = """
            SELECT
                fm.registro,
                fm.fome_empr,
                fm.fome_fili,
                fm.fome_func,
                fm.fome_refe,
                fm.fome_even,
                fm.fome_base,
                fm.fome_perc,
                fm.fome_valo,
                fm.fome_tipo,
                fm.fome_tipo_base,

                fu.func_nome,
                fu.func_cpf,
                fu.func_pis,
                fu.func_carg,
                fu.func_depa,
                fu.func_seto,
                fu.func_sind,
                fu.func_deir,
                fu.func_irrf,
                fu.func_inss,
                fu.func_fgts,

                ev.even_desc,
                ev.even_tipo,
                ev.even_inss,
                ev.even_irrf,
                ev.even_fgts,
                ev.even_rais,
                ev.even_dedu,

                ca.carg_nome,
                de.depa_nome,
                se.seto_desc,
                si.sind_nome

            FROM folhamensal fm

            LEFT JOIN funcionarios fu
              ON fu.registro = fm.registro
             AND fu.func_empr = fm.fome_empr
             AND fu.func_fili = fm.fome_fili
             AND fu.func_codi = fm.fome_func

            LEFT JOIN eventos ev
              ON ev.registro = fm.registro
             AND ev.even_empr = fm.fome_empr
             AND ev.even_codi = fm.fome_even

            LEFT JOIN cargos ca
              ON ca.registro = fm.registro
             AND ca.carg_codi = fu.func_carg

            LEFT JOIN departamentosrh de
              ON de.registro = fm.registro
             AND de.depa_empr = fm.fome_empr
             AND de.depa_codi = fu.func_depa

            LEFT JOIN setoresrh se
              ON se.registro = fm.registro
             AND se.seto_empr = fm.fome_empr
             AND se.seto_codi = fu.func_seto

            LEFT JOIN sindicatos si
              ON si.registro = fm.registro
             AND si.sind_codi = fu.func_sind

            WHERE fm.registro = %s
              AND fm.fome_empr = %s
              AND fm.fome_refe = %s
        """

        params = [registro, empresa, referencia]

        if filial:
            sql += " AND fm.fome_fili = %s"
            params.append(filial)

        if funcionario:
            sql += " AND fm.fome_func = %s"
            params.append(funcionario)

        if nome:
            sql += " AND fu.func_nome ILIKE %s"
            params.append(f"%{nome}%")

        sql += """
            ORDER BY
                fu.func_nome,
                fm.fome_func,
                fm.fome_even
        """

        with connections[db_alias].cursor() as cursor:
            cursor.execute(sql, params)
            cols = [col[0] for col in cursor.description]
            return [dict(zip(cols, row)) for row in cursor.fetchall()]

    @classmethod
    def resumo_funcionarios(cls, *, db_alias, registro, empresa, referencia, filial=None, nome=None):
        lancamentos = cls.listar_lancamentos(
            db_alias=db_alias,
            registro=registro,
            empresa=empresa,
            referencia=referencia,
            filial=filial,
            nome=nome,
        )

        por_funcionario = {}

        for item in lancamentos:
            chave = (
                item["registro"],
                item["fome_empr"],
                item["fome_fili"],
                item["fome_func"],
                item["fome_refe"],
            )

            if chave not in por_funcionario:
                por_funcionario[chave] = {
                    "registro": item["registro"],
                    "empresa": item["fome_empr"],
                    "filial": item["fome_fili"],
                    "referencia": item["fome_refe"],
                    "funcionario_id": item["fome_func"],
                    "funcionario_nome": item["func_nome"],
                    "cpf": item["func_cpf"],
                    "pis": item["func_pis"],
                    "cargo": item["carg_nome"],
                    "departamento": item["depa_nome"],
                    "setor": item["seto_desc"],
                    "sindicato": item["sind_nome"],
                    "proventos": D0,
                    "descontos": D0,
                    "base_inss": D0,
                    "base_irrf": D0,
                    "base_fgts": D0,
                    "fgts_estimado": D0,
                    "liquido": D0,
                    "eventos": [],
                }

            resumo = por_funcionario[chave]
            valor = valores(item["fome_valo"])
            tipo = cls._classificar_tipo(item)

            if tipo == "desconto":
                resumo["descontos"] += valor
            else:
                resumo["proventos"] += valor

            if item.get("even_inss"):
                resumo["base_inss"] += cls._valor_base_tributavel(valor, tipo)

            if item.get("even_irrf"):
                resumo["base_irrf"] += cls._valor_base_tributavel(valor, tipo)

            if item.get("even_fgts"):
                resumo["base_fgts"] += cls._valor_base_tributavel(valor, tipo)

            resumo["eventos"].append({
                "codigo": item["fome_even"],
                "descricao": item["even_desc"],
                "tipo": tipo,
                "base": valores(item["fome_base"]),
                "percentual": item["fome_perc"],
                "valor": valor,
                "incide_inss": bool(item.get("even_inss")),
                "incide_irrf": bool(item.get("even_irrf")),
                "incide_fgts": bool(item.get("even_fgts")),
            })

        for resumo in por_funcionario.values():
            resumo["fgts_estimado"] = valores(resumo["base_fgts"] * Decimal("0.08"))
            resumo["liquido"] = valores(resumo["proventos"] - resumo["descontos"])

        return list(por_funcionario.values())

    @classmethod
    def conferencia_tributos(cls, *, db_alias, registro, empresa, referencia, filial=None, funcionario=None):
        resumos = cls.resumo_funcionarios(
            db_alias=db_alias,
            registro=registro,
            empresa=empresa,
            referencia=referencia,
            filial=filial,
        )

        if funcionario:
            resumos = [r for r in resumos if r["funcionario_id"] == funcionario]

        tabela_inss = cls._buscar_tabela_inss(db_alias=db_alias, referencia=referencia)
        tabela_irrf = cls._buscar_tabela_irrf(db_alias=db_alias, referencia=referencia)

        resultado = []

        for resumo in resumos:
            dependentes_irrf = cls._contar_dependentes_irrf(
                db_alias=db_alias,
                registro=registro,
                empresa=empresa,
                funcionario=resumo["funcionario_id"],
            )

            inss = cls.calcular_inss_progressivo(
                base=resumo["base_inss"],
                tabela=tabela_inss,
            )

            irrf = cls.calcular_irrf(
                base_irrf=resumo["base_irrf"],
                valor_inss=inss["valor"],
                dependentes=dependentes_irrf,
                tabela=tabela_irrf,
            )

            resultado.append({
                **resumo,
                "dependentes_irrf": dependentes_irrf,
                "inss_calculado": inss,
                "irrf_calculado": irrf,
            })

        return resultado

    @staticmethod
    def calcular_inss_progressivo(*, base, tabela):
        base = valores(base)

        if not tabela:
            return {
                "base": base,
                "valor": D0,
                "faixas": [],
                "observacao": "Tabela INSS não encontrada para a referência.",
            }

        faixas = [
            (valores(tabela.get("tabe_fa01")), valores(tabela.get("tabe_pe01"))),
            (valores(tabela.get("tabe_fa02")), valores(tabela.get("tabe_pe02"))),
            (valores(tabela.get("tabe_fa03")), valores(tabela.get("tabe_pe03"))),
            (valores(tabela.get("tabe_fa04")), valores(tabela.get("tabe_pe04"))),
        ]

        teto = valores(tabela.get("tabe_maxr"))
        if teto > 0 and base > teto:
            base_calculo = teto
        else:
            base_calculo = base

        total = D0
        anterior = D0
        detalhes = []

        for limite, aliquota in faixas:
            if limite <= 0 or aliquota <= 0:
                continue

            faixa_base = min(base_calculo, limite) - anterior

            if faixa_base > 0:
                valor_faixa = valores(faixa_base * (aliquota / Decimal("100")))
                total += valor_faixa

                detalhes.append({
                    "de": anterior,
                    "ate": limite,
                    "base": faixa_base,
                    "aliquota": aliquota,
                    "valor": valor_faixa,
                })

            anterior = limite

            if base_calculo <= limite:
                break

        desconto_maximo = valores(tabela.get("tabe_dema"))

        if desconto_maximo > 0 and total > desconto_maximo:
            total = desconto_maximo

        return {
            "base": base,
            "base_calculo": base_calculo,
            "valor": valores(total),
            "faixas": detalhes,
            "teto": teto,
            "desconto_maximo": desconto_maximo,
        }

    @staticmethod
    def calcular_irrf(*, base_irrf, valor_inss, dependentes, tabela):
        base_irrf = valores(base_irrf)
        valor_inss = valores(valor_inss)

        if not tabela:
            return {
                "base": base_irrf,
                "base_calculo": D0,
                "valor": D0,
                "observacao": "Tabela IRRF não encontrada para a referência.",
            }

        deducao_dependente = valores(tabela.get("irrf_dede"))
        dependentes = int(dependentes or 0)

        base_calculo = valores(
            base_irrf
            - valor_inss
            - (deducao_dependente * Decimal(dependentes))
        )

        if base_calculo <= 0:
            return {
                "base": base_irrf,
                "base_calculo": D0,
                "valor": D0,
                "dependentes": dependentes,
                "deducao_dependente": deducao_dependente,
            }

        faixas = [
            (valores(tabela.get("irrf_fa01")), valores(tabela.get("irrf_pe01")), valores(tabela.get("irrf_de01"))),
            (valores(tabela.get("irrf_fa02")), valores(tabela.get("irrf_pe02")), valores(tabela.get("irrf_de02"))),
            (valores(tabela.get("irrf_fa03")), valores(tabela.get("irrf_pe03")), valores(tabela.get("irrf_de03"))),
            (valores(tabela.get("irrf_fa04")), valores(tabela.get("irrf_pe04")), valores(tabela.get("irrf_de04"))),
        ]

        aliquota = D0
        deducao = D0

        for limite, perc, ded in faixas:
            if limite > 0 and base_calculo <= limite:
                aliquota = perc
                deducao = ded
                break

            aliquota = perc
            deducao = ded

        valor = valores((base_calculo * (aliquota / Decimal("100"))) - deducao)

        if valor < 0:
            valor = D0

        return {
            "base": base_irrf,
            "base_calculo": base_calculo,
            "valor": valor,
            "aliquota": aliquota,
            "deducao": deducao,
            "dependentes": dependentes,
            "deducao_dependente": deducao_dependente,
        }

    @staticmethod
    def totais_gerais(conferencias):
        totais = {
            "funcionarios": len(conferencias),
            "proventos": D0,
            "descontos": D0,
            "liquido": D0,
            "base_inss": D0,
            "inss": D0,
            "base_irrf": D0,
            "irrf": D0,
            "base_fgts": D0,
            "fgts": D0,
        }

        for item in conferencias:
            totais["proventos"] += item["proventos"]
            totais["descontos"] += item["descontos"]
            totais["liquido"] += item["liquido"]
            totais["base_inss"] += item["base_inss"]
            totais["inss"] += item["inss_calculado"]["valor"]
            totais["base_irrf"] += item["base_irrf"]
            totais["irrf"] += item["irrf_calculado"]["valor"]
            totais["base_fgts"] += item["base_fgts"]
            totais["fgts"] += item["fgts_estimado"]

        return {k: valores(v) if k != "funcionarios" else v for k, v in totais.items()}

    @staticmethod
    def _buscar_tabela_inss(*, db_alias, referencia):
        with connections[db_alias].cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM tabelainss
                WHERE tabe_refe <= %s
                ORDER BY tabe_refe DESC
                LIMIT 1
                """,
                [referencia],
            )
            row = cursor.fetchone()
            if not row:
                return None

            cols = [col[0] for col in cursor.description]
            return dict(zip(cols, row))

    @staticmethod
    def _buscar_tabela_irrf(*, db_alias, referencia):
        with connections[db_alias].cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM tabelairrf
                WHERE irrf_refe <= %s
                ORDER BY irrf_refe DESC
                LIMIT 1
                """,
                [referencia],
            )
            row = cursor.fetchone()
            if not row:
                return None

            cols = [col[0] for col in cursor.description]
            return dict(zip(cols, row))

    @staticmethod
    def _contar_dependentes_irrf(*, db_alias, registro, empresa, funcionario):
        with connections[db_alias].cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM dependentesrh
                WHERE registro = %s
                  AND depe_empr = %s
                  AND depe_func = %s
                  AND COALESCE(depe_inca, false) = true
                """,
                [registro, empresa, funcionario],
            )
            return cursor.fetchone()[0] or 0

    @staticmethod
    def _classificar_tipo(item):
        tipo_folha = str(item.get("fome_tipo") or "").upper().strip()
        tipo_evento = str(item.get("even_tipo") or "").upper().strip()

        descontos = {"D", "2", "-", "S"}
        proventos = {"P", "1", "+", "E", "V"}

        if tipo_folha in descontos:
            return "desconto"

        if tipo_evento in descontos:
            return "desconto"

        if tipo_folha in proventos:
            return "provento"

        if tipo_evento in proventos:
            return "provento"

        return "provento"

    @staticmethod
    def _valor_base_tributavel(valor, tipo):
        valor = valores(valor)

        if tipo == "desconto":
            return -valor

        return valor