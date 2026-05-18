from django.db import models
from core.consultas import BancoConsulta

class Sindicatos(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    sind_codi = models.IntegerField()
    sind_nome = models.CharField(max_length=100, blank=True, null=True)
    sind_cnpj = models.CharField(max_length=14, blank=True, null=True)
    sind_codi_sind = models.CharField(max_length=15, blank=True, null=True)
    sind_cida = models.CharField(max_length=60, blank=True, null=True)
    sind_esta = models.CharField(max_length=2, blank=True, null=True)
    sind_fone = models.CharField(max_length=14, blank=True, null=True)
    sind_emai = models.CharField(max_length=100, blank=True, null=True)
    sind_mes_conv = models.IntegerField(blank=True, null=True)
    sind_perc_desc_mens = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sind_max_desc_vt = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sind_mese_medi = models.IntegerField(blank=True, null=True)
    sind_even_desc = models.IntegerField(blank=True, null=True)
    sind_piso_cate = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    sind_obse = models.TextField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.   
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.   
    sind_adic_temp_serv = models.BooleanField(blank=True, null=True)
    sind_medi_feri = models.IntegerField(blank=True, null=True)
    sind_porc_adic = models.IntegerField(blank=True, null=True)
    sind_peri_adic = models.IntegerField(blank=True, null=True)
    sind_porc_adic_maxi = models.IntegerField(blank=True, null=True)
    
    objects = BancoConsulta()   
    
    class Meta:
        managed = False
        db_table = 'sindicatos'
        unique_together = (('registro', 'sind_codi'),)

# Create your models here.
