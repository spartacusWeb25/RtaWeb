from django.db import models
from core.consultas import BancoConsulta

class Tabelasalariominimo(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    refe_empr = models.IntegerField()
    refe_sala_mini_fede = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    refe_sala_mini_esta = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    refe_sala_ref1 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    refe_sala_ref2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.

    objects = BancoConsulta()   
    
    class Meta:
        managed = False
        db_table = 'tabelasalariominimo'
        unique_together = (('registro', 'refe_empr'),)

# Create your models here.
