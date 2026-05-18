from django.db import models
from core.consultas import BancoConsulta

class Lancamentosfolha(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    lafo_empr = models.SmallIntegerField()
    lafo_refe = models.CharField(max_length=6)
    lafo_func = models.IntegerField()
    lafo_even = models.IntegerField()
    lafo_base = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    lafo_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    lafo_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_obse = models.TextField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.   
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.   
    lafo_same = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_saho = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lafo_tipo = models.CharField(max_length=1, blank=True, null=True)

    objects = BancoConsulta()   
    
    class Meta:
        managed = False
        db_table = 'lancamentosfolha'
        unique_together = (('registro', 'lafo_empr', 'lafo_refe', 'lafo_func', 'lafo_even'),)

# Create your models here.
