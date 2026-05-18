from django.db import models
from core.consultas import BancoConsulta

class Tabelasalarial(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    tasa_empr = models.IntegerField()
    tasa_func = models.IntegerField()
    tasa_refe = models.CharField(max_length=6)
    tasa_same = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tasa_saho = models.DecimalField(max_digits=15, decimal_places=8, blank=True, null=True)
    tasa_carg = models.IntegerField(blank=True, null=True)
    tasa_depa = models.IntegerField(blank=True, null=True)
    tasa_seto = models.IntegerField(blank=True, null=True)
    tasa_sind = models.IntegerField(blank=True, null=True)
    tasa_home = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tasa_hose = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tasa_moti_carg = models.TextField(blank=True, null=True)
    tasa_moti_depa = models.TextField(blank=True, null=True)
    tasa_moti_sala = models.TextField(blank=True, null=True)
    tasa_dirf = models.IntegerField(blank=True, null=True)
    tasa_dsaf = models.IntegerField(blank=True, null=True)
    tasa_obse = models.TextField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.   
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.   
    tasa_moti_seto = models.TextField(blank=True, null=True)
    tasa_redu_jorn = models.IntegerField(blank=True, null=True)
    tasa_dias_dura = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    objects = BancoConsulta()

    class Meta:
        managed = False
        db_table = 'tabelasalarial'
        unique_together = (('registro', 'tasa_empr', 'tasa_func', 'tasa_refe'),)


# Create your models here.
