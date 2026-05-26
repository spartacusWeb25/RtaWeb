from django.db import models
from core.consultas import BancoConsulta

class Usuarios(models.Model):
    id = models.IntegerField()
    usua_nome = models.CharField(max_length=60, blank=True, null=True)
    usua_login = models.CharField(max_length=60, blank=True, null=True)
    usua_senh = models.CharField(max_length=60, blank=True, null=True)
    usua_emai = models.CharField(max_length=60, blank=True, null=True)
    usua_ativ = models.BooleanField(blank=True, null=True)
    usua_grup = models.IntegerField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.   
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.   
    registro = models.CharField(max_length=14, db_column='registro', primary_key=True)
    super = models.BooleanField(blank=True, null=True)

    objects = BancoConsulta()   
   
    class Meta:
        managed = False
        db_table = 'usuarios'
        unique_together = (('registro', 'id'),)
# Create your models here.
