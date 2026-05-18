from django.db import models
from core.consultas import BancoConsulta

class Cargos(models.Model):
    registro = models.CharField(max_length=14)
    carg_codi = models.IntegerField()
    carg_cbo = models.CharField(max_length=7, blank=True, null=True)
    carg_nome = models.CharField(max_length=60, blank=True, null=True)
    carg_obse = models.TextField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    objects = BancoConsulta()   
   
    class Meta:
        managed = False
        db_table = 'cargos'


# Create your models here.
