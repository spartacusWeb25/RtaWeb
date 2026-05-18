from django.db import models
from core.consultas import BancoConsulta

class Adtodecimo(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    adto_empr = models.IntegerField()
    adto_func = models.IntegerField()
    adto_ano = models.IntegerField()
    adto_data = models.DateField(blank=True, null=True)
    adto_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    adto_perc_fgts = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    adto_fgts = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    adto_orig = models.CharField(max_length=1, blank=True, null=True)
    adto_obse = models.TextField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.   
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  
    
    objects = BancoConsulta()   
   
    class Meta:
        managed = False
        db_table = 'adtodecimo'
        unique_together = (('registro', 'adto_empr', 'adto_func', 'adto_ano'),)


# Create your models here.
