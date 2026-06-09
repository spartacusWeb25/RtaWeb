from django.db import models
from core.consultas import BancoConsulta

class Cargos(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    carg_codi = models.IntegerField()
    carg_cbo = models.CharField(max_length=7, blank=True, null=True)
    carg_nome = models.CharField(max_length=60, blank=True, null=True)
    carg_obse = models.TextField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)

    objects = BancoConsulta()   
    
    class Meta:
        managed = False
        db_table = 'cargos'
        unique_together = (('registro', 'carg_codi'),)


# Create your models here.
