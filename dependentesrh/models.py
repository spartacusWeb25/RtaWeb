from django.db import models
from core.consultas import BancoConsulta

class Dependentesrh(models.Model):
    registro = models.ForeignKey('Funcionarios', models.DO_NOTHING, db_column='registro', primary_key=True)
    depe_empr = models.IntegerField()
    depe_func = models.IntegerField()
    depe_nome = models.CharField(max_length=60, blank=True, null=True)
    depe_sexo = models.CharField(max_length=1, blank=True, null=True)
    depe_tipo = models.IntegerField(blank=True, null=True)
    depe_dana = models.DateField(blank=True, null=True)
    depe_sate = models.DateField(blank=True, null=True)
    depe_iate = models.DateField(blank=True, null=True)
    depe_pate = models.DateField(blank=True, null=True)
    depe_obse = models.TextField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.   
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.   
    depe_codi = models.IntegerField()
    depe_cpf = models.CharField(max_length=11, blank=True, null=True)
    depe_inca = models.BooleanField(blank=True, null=True)

    objects = BancoConsulta()   
    
    class Meta:
        managed = False
        db_table = 'dependentesrh'
        unique_together = (('registro', 'depe_empr', 'depe_func', 'depe_codi'),)
