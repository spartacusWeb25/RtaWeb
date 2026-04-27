import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = "Gera JSON com schema e arquivo models.py estilo inspectdb"

    def add_arguments(self, parser):
        parser.add_argument("--db", default="default")
        parser.add_argument("--schema", default="public")
        parser.add_argument("--saida-json", default="schema_folha.json")
        parser.add_argument("--saida-models", default="models_inspect.py")
        parser.add_argument("--folha", action="store_true")

    def handle(self, *args, **options):
        db_alias = options["db"]
        schema = options["schema"]
        saida_json = options["saida_json"]
        saida_models = options["saida_models"]
        somente_folha = options["folha"]

        if db_alias not in connections:
            self.stderr.write(self.style.ERROR(f"Banco '{db_alias}' não existe."))
            return

        palavras_folha = [
            "folha", "funcionario", "funcionarios", "rh", "ferias",
            "rescisao", "decimo", "adi", "eventos", "cargos",
            "setores", "departamentos", "dependentes", "sefip",
            "rais", "caged", "esocial", "inss", "irrf",
            "sindicatos", "horarios", "jornada", "valetransporte",
            "valerefeicao", "lctofolha", "lancamentosfolha",
        ]

        resultado = {
            "db_alias": db_alias,
            "schema": schema,
            "total_tabelas": 0,
            "tabelas": {},
        }

        with connections[db_alias].cursor() as cursor:
            cursor.execute(
                """
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = %s
                ORDER BY tablename;
                """,
                [schema],
            )
            tabelas = [row[0] for row in cursor.fetchall()]

            if somente_folha:
                tabelas = [
                    tabela for tabela in tabelas
                    if any(p in tabela.lower() for p in palavras_folha)
                ]

            resultado["total_tabelas"] = len(tabelas)

            for tabela in tabelas:
                cursor.execute(
                    """
                    SELECT
                        column_name,
                        data_type,
                        udt_name,
                        is_nullable,
                        column_default,
                        character_maximum_length,
                        numeric_precision,
                        numeric_scale
                    FROM information_schema.columns
                    WHERE table_schema = %s
                      AND table_name = %s
                    ORDER BY ordinal_position;
                    """,
                    [schema, tabela],
                )

                campos = []
                for row in cursor.fetchall():
                    campos.append({
                        "nome": row[0],
                        "tipo": row[1],
                        "tipo_postgres": row[2],
                        "nulo": row[3] == "YES",
                        "default": row[4],
                        "tamanho": row[5],
                        "precisao": row[6],
                        "escala": row[7],
                    })

                resultado["tabelas"][tabela] = {
                    "total_campos": len(campos),
                    "campos": campos,
                }

        Path(saida_json).write_text(
            json.dumps(resultado, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        Path(saida_models).write_text(
            self.gerar_models(resultado),
            encoding="utf-8",
        )

        self.stdout.write(self.style.SUCCESS(f"JSON gerado: {Path(saida_json).resolve()}"))
        self.stdout.write(self.style.SUCCESS(f"Models gerado: {Path(saida_models).resolve()}"))
        self.stdout.write(self.style.SUCCESS(f"Total de tabelas: {resultado['total_tabelas']}"))

    def gerar_models(self, resultado):
        linhas = [
            "from django.db import models",
            "",
            "",
        ]

        for tabela, dados in resultado["tabelas"].items():
            classe = self.nome_classe(tabela)

            linhas.append(f"class {classe}(models.Model):")

            if not dados["campos"]:
                linhas.append("    pass")
            else:
                for campo in dados["campos"]:
                    linhas.append(self.gerar_campo(campo))

            linhas.append("")
            linhas.append("    class Meta:")
            linhas.append("        managed = False")
            linhas.append(f"        db_table = '{tabela}'")
            linhas.append("")
            linhas.append("")

        return "\n".join(linhas)

    def nome_classe(self, tabela):
        partes = re.split(r"[^a-zA-Z0-9]+", tabela)
        nome = "".join(p.capitalize() for p in partes if p)

        if not nome:
            nome = "TabelaLegada"

        if nome[0].isdigit():
            nome = f"Tabela{nome}"

        return nome

    def nome_campo(self, nome):
        nome_limpo = re.sub(r"[^a-zA-Z0-9_]", "_", nome)

        if nome_limpo[0].isdigit():
            nome_limpo = f"campo_{nome_limpo}"

        return nome_limpo

    def tipo_django(self, campo):
        tipo = campo["tipo"]
        tipo_pg = campo["tipo_postgres"]

        if tipo_pg in ("int2",):
            return "models.SmallIntegerField"
        if tipo_pg in ("int4", "serial"):
            return "models.IntegerField"
        if tipo_pg in ("int8", "bigserial"):
            return "models.BigIntegerField"
        if tipo_pg in ("varchar", "bpchar"):
            return "models.CharField"
        if tipo_pg in ("text",):
            return "models.TextField"
        if tipo_pg in ("bool",):
            return "models.BooleanField"
        if tipo_pg in ("date",):
            return "models.DateField"
        if tipo_pg in ("timestamp", "timestamptz"):
            return "models.DateTimeField"
        if tipo_pg in ("numeric", "decimal", "money"):
            return "models.DecimalField"
        if tipo_pg in ("float4", "float8"):
            return "models.FloatField"
        if tipo_pg in ("time", "timetz"):
            return "models.TimeField"
        if tipo_pg in ("json", "jsonb"):
            return "models.JSONField"
        if tipo_pg in ("uuid",):
            return "models.UUIDField"

        if tipo == "character varying":
            return "models.CharField"
        if tipo == "integer":
            return "models.IntegerField"
        if tipo == "numeric":
            return "models.DecimalField"

        return "models.TextField"

    def gerar_campo(self, campo):
        nome_original = campo["nome"]
        nome_python = self.nome_campo(nome_original)
        field = self.tipo_django(campo)

        args = []

        if nome_original == "id":
            return "    id = models.AutoField(primary_key=True)"

        if nome_python != nome_original:
            args.append(f"db_column='{nome_original}'")

        if field == "models.CharField":
            args.append(f"max_length={campo['tamanho'] or 255}")

        if field == "models.DecimalField":
            args.append(f"max_digits={campo['precisao'] or 15}")
            args.append(f"decimal_places={campo['escala'] or 2}")

        if campo["nulo"]:
            args.append("blank=True")
            args.append("null=True")

        args_str = ", ".join(args)

        return f"    {nome_python} = {field}({args_str})"



#rodar completo python manage.py listar_tabelas --db=default --saida-json=schema_completo.json --saida-models=models_completo.py
#rodar só folha python manage.py listar_tabelas --db=default --folha --saida-json=schema_folha.json --saida-models=models_folha.py
