from django.db import models
from core.consultas import BancoConsulta
from core.utils import format_month_reference

class Tabelasalafami(models.Model):
    safa_refe = models.CharField(primary_key=True, max_length=6)
    safa_fa01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    safa_co01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    safa_fa02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    safa_co02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
    objects = BancoConsulta()   
    
    class Meta:
        managed = False
        db_table = 'tabelasalafami'

    @property
    def safa_refe_formatada(self):
        return format_month_reference(self.safa_refe)
