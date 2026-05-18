from django.db import models
from core.consultas import BancoConsulta


class Setoresrh(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    seto_empr = models.IntegerField()
    seto_codi = models.IntegerField()
    seto_desc = models.CharField(max_length=60, blank=True, null=True)
    seto_sigl = models.CharField(max_length=5, blank=True, null=True)
    seto_cecu = models.IntegerField(blank=True, null=True)
    seto_obse = models.TextField(blank=True, null=True)
    
    objects = BancoConsulta()   
    
    class Meta:
        managed = False
        db_table = 'setoresrh'
        unique_together = (('registro', 'seto_empr', 'seto_codi'),)
    
    def __str__(self):
        return self.seto_desc
   