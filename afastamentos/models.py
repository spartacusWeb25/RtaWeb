from django.db import models
from core.consultas import BancoConsulta

class Afastamentos(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    afas_empr = models.IntegerField()
    afas_func = models.IntegerField()
    afas_ctrl = models.IntegerField()
    afas_said = models.DateField(blank=True, null=True)
    afas_codi_said = models.CharField(max_length=2, blank=True, null=True)
    afas_reto = models.DateField(blank=True, null=True)
    afas_codi_reto = models.CharField(max_length=2, blank=True, null=True)
    afas_obse = models.CharField(max_length=255, blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.   
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.   
    afas_tipo = models.IntegerField(blank=True, null=True)
    afas_tipo_esoc = models.CharField(max_length=2, blank=True, null=True)
    afas_msmm = models.IntegerField()
    afas_tpac = models.IntegerField()
    afas_ates_ccid = models.CharField(max_length=4, blank=True, null=True)
    afas_ates_dias = models.IntegerField(blank=True, null=True)
    afas_ates_emit = models.CharField(max_length=70, blank=True, null=True)
    afas_ates_clas = models.IntegerField()
    afas_ates_insc = models.CharField(max_length=14, blank=True, null=True)
    afas_ates_ufoc = models.CharField(max_length=2, blank=True, null=True)
    afas_cere_cnpj = models.CharField(max_length=14, blank=True, null=True)
    afas_cere_onus = models.IntegerField()
    afas_sind_cnpj = models.CharField(max_length=14, blank=True, null=True)
    afas_sind_onre = models.IntegerField()
    
    objects = BancoConsulta()      

    class Meta:
        managed = False
        db_table = 'afastamentos'
        unique_together = (('registro', 'afas_empr', 'afas_func', 'afas_ctrl'),)


# Create your models here.
