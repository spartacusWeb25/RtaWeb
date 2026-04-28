from django.db import models
from core.consultas import BancoConsulta

# Create your models here.
class Tabelainss(models.Model):
    tabe_refe = models.CharField(max_length=6)
    tabe_fa01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_pe01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_fa02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_pe02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_fa03 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_pe03 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_fa04 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_pe04 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_dema = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_maxr = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    objects = BancoConsulta()
    
    class Meta:
        managed = False
        db_table = 'tabelainss'


class Tabelainssempresa(models.Model):
    tabe_empr = models.IntegerField()
    tabe_cont_empr = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_rat = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_terc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_prop_auto = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_grps_terc = models.IntegerField(blank=True, null=True)
    tabe_grps_rat = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tabe_cnae = models.CharField(max_length=10, blank=True, null=True)
    tabe_simp = models.BooleanField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)
    tabe_grps_fpas = models.CharField(max_length=8, blank=True, null=True)
    tabe_fap = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    registro = models.CharField(max_length=14)
    
    
    objects = BancoConsulta()

    class Meta:
        managed = False
        db_table = 'tabelainssempresa'


class Tabelairrf(models.Model):
    irrf_refe = models.CharField(max_length=6, primary_key=True)
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
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    objects = BancoConsulta()
    
    class Meta:
        managed = False
        db_table = 'tabelairrf'
