from django.db import models
from core.consultas import BancoConsulta

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

# Create your models here.
