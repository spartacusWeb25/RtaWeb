from django.db import models
from django.db import connection
from django.utils import timezone


def _digits_only(valor) -> str:
    if valor is None:
        return ""
    return "".join(ch for ch in str(valor) if ch.isdigit())


class Horarios(models.Model):
    registro = models.CharField(max_length=14, primary_key=True, db_column="registro")
    hora_empr = models.IntegerField(default=0)
    hora_fili = models.IntegerField(default=0)
    hora_codi = models.IntegerField(default=0)

    hora_nome = models.CharField(max_length=250, blank=True, null=True)
    hora_flexivel = models.BooleanField(default=False, blank=True, null=True)
    hora_total_semana = models.CharField(max_length=10, blank=True, null=True)
    hora_folga_alt = models.BooleanField(default=False, blank=True, null=True)

    hora_folga_dom = models.BooleanField(default=False, blank=True, null=True)
    hora_folga_seg = models.BooleanField(default=False, blank=True, null=True)
    hora_folga_ter = models.BooleanField(default=False, blank=True, null=True)
    hora_folga_qua = models.BooleanField(default=False, blank=True, null=True)
    hora_folga_qui = models.BooleanField(default=False, blank=True, null=True)
    hora_folga_sex = models.BooleanField(default=False, blank=True, null=True)
    hora_folga_sab = models.BooleanField(default=False, blank=True, null=True)

    hora_desc_esocial = models.TextField(blank=True, null=True)

    _DIAS = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"]
    _CAMPOS_POR_DIA = [
        "esoc",
        "inic_1", "fina_1",
        "lanc_inic_1", "lanc_fina_1",
        "inic_2", "fina_2",
        "lanc_inic_2", "lanc_fina_2",
        "intervalo", "jornada",
    ]

    for _d in _DIAS:
        for _c in _CAMPOS_POR_DIA:
            _nome_campo = f"hora_{_d}_{_c}"
            if _c == "esoc":
                locals()[_nome_campo] = models.IntegerField(blank=True, null=True)
            else:
                locals()[_nome_campo] = models.CharField(max_length=10, blank=True, null=True)

    _log_data = models.DateField(db_column="_log_data", blank=True, null=True)
    _log_time = models.TimeField(db_column="_log_time", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "horarios"

    def _todos_campos_coluna(self):
        campos = [
            "registro", "hora_empr", "hora_fili", "hora_codi",
            "hora_nome", "hora_flexivel", "hora_total_semana",
            "hora_folga_alt",
            "hora_folga_dom", "hora_folga_seg", "hora_folga_ter",
            "hora_folga_qua", "hora_folga_qui", "hora_folga_sex", "hora_folga_sab",
            "hora_desc_esocial",
        ]
        for d in self._DIAS:
            for c in self._CAMPOS_POR_DIA:
                campos.append(f"hora_{d}_{c}")
        campos.extend(["_log_data", "_log_time"])
        return campos

    def _valor_para_sql(self, nome_campo):
        valor = getattr(self, nome_campo, None)
        if nome_campo == "registro":
            return _digits_only(valor)[:14] or None
        if isinstance(valor, bool):
            return valor
        return valor

    def save(self, *args, operacao=None, db_alias="default", **kwargs):
        if not operacao:
            raise RuntimeError("Horarios.save requer operacao='criar' ou 'editar'")

        self.registro = _digits_only(self.registro)[:14]
        if not self.registro:
            raise RuntimeError("Horarios.save: registro vazio")

        agora = timezone.now()
        self._log_data = agora.date()
        self._log_time = agora.time()

        todos_campos = self._todos_campos_coluna()
        colunas = [c for c in todos_campos if c != "registro"]
        placeholders = ", ".join(["%s"] * len(colunas))

        valores = []
        for c in colunas:
            valores.append(self._valor_para_sql(c))

        reg = self._valor_para_sql("registro")
        empr = int(self.hora_empr or 0)
        fili = int(self.hora_fili or 0)
        codi = int(self.hora_codi or 0)

        with connection.cursor() as cursor:
            if operacao == "criar":
                existe_sql = (
                    "SELECT 1 FROM public.horarios "
                    "WHERE registro=%s AND hora_empr=%s AND hora_fili=%s AND hora_codi=%s LIMIT 1"
                )
                cursor.execute(existe_sql, [reg, empr, fili, codi])
                if cursor.fetchone() is not None:
                    raise RuntimeError(
                        f"Já existe Horario com PK ({reg}, {empr}, {fili}, {codi})"
                    )

                colunas_insert = ["registro"] + colunas
                placeholders_insert = ", ".join(["%s"] * len(colunas_insert))
                sql_insert = (
                    f"INSERT INTO public.horarios ({', '.join(colunas_insert)}) "
                    f"VALUES ({placeholders_insert})"
                )
                params = [reg] + valores
                cursor.execute(sql_insert, params)

            elif operacao == "editar":
                sets = ", ".join([f"{c} = %s" for c in colunas])
                sql_update = (
                    f"UPDATE public.horarios SET {sets} "
                    f"WHERE registro=%s AND hora_empr=%s AND hora_fili=%s AND hora_codi=%s"
                )
                params = valores + [reg, empr, fili, codi]
                cursor.execute(sql_update, params)

            else:
                raise RuntimeError(f"Horarios.save operacao invalida: {operacao}")

    def delete(self, *args, db_alias="default", **kwargs):
        reg = _digits_only(self.registro)[:14]
        empr = int(self.hora_empr or 0)
        fili = int(self.hora_fili or 0)
        codi = int(self.hora_codi or 0)
        if not reg:
            raise RuntimeError("Horarios.delete: registro vazio")

        sql = (
            "DELETE FROM public.horarios "
            "WHERE registro=%s AND hora_empr=%s AND hora_fili=%s AND hora_codi=%s"
        )
        with connection.cursor() as cursor:
            cursor.execute(sql, [reg, empr, fili, codi])
