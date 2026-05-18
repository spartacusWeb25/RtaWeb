from django.db import models
from core.consultas import BancoConsulta

class Tabelairrf(models.Model):
    irrf_refe = models.CharField(primary_key=True, max_length=6)
    irrf_fa01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_pe01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_fa02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_pe02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_fa03 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_pe03 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_fa04 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_pe04 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_de01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_de02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_de03 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_de04 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_dede = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_isen = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    irrf_demi = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.
    field_log_time = models.DateField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.

    objects = BancoConsulta()   

    class Meta:
        managed = False
        db_table = 'tabelairrf'