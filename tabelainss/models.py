from django.db import models
from core.consultas import BancoConsulta

# Create your models here.
class Tabelainss(models.Model):
    tabe_refe = models.CharField(max_length=6, primary_key=True)
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

# Create your models here.
