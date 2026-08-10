from django.db import models
from core.consultas import BancoConsulta


class Dependentesrh(models.Model):
    registro = models.CharField(max_length=14, primary_key=True)
    depe_empr = models.IntegerField()
    depe_fili = models.IntegerField()
    depe_func = models.IntegerField()
    depe_codi = models.IntegerField()

    depe_nome = models.CharField(max_length=120, blank=True, null=True)
    depe_nascimento = models.DateField(blank=True, null=True)
    depe_cpf = models.CharField(max_length=11, blank=True, null=True)
    depe_matricula = models.CharField(max_length=30, blank=True, null=True)
    depe_local_nascimento = models.CharField(max_length=60, blank=True, null=True)
    depe_cidade_codigo = models.IntegerField(blank=True, null=True)
    depe_cidade = models.CharField(max_length=60, blank=True, null=True)
    depe_cartorio = models.CharField(max_length=120, blank=True, null=True)
    depe_numero_registro = models.CharField(max_length=20, blank=True, null=True)
    depe_numero_livro = models.CharField(max_length=20, blank=True, null=True)
    depe_numero_folha = models.CharField(max_length=20, blank=True, null=True)
    depe_data_entrega = models.DateField(blank=True, null=True)
    depe_tipo_dependencia = models.IntegerField(blank=True, null=True)
    depe_data_baixa = models.DateField(blank=True, null=True)
    depe_ir_ate = models.CharField(max_length=7, blank=True, null=True)
    depe_tipo_dependente = models.IntegerField(blank=True, null=True)
    depe_invalido = models.BooleanField(default=False, blank=True, null=True)
    depe_observacoes = models.TextField(blank=True, null=True)

    objects = BancoConsulta()

    class Meta:
        managed = False
        db_table = "dependentesrh"
        unique_together = (
            ("registro", "depe_empr", "depe_fili", "depe_func", "depe_codi"),
        )

    def __str__(self):
        return self.depe_nome or f"Dependente #{self.depe_codi}"
