from django.db import models
from core.consultas import BancoConsulta

class Eventos(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    even_codi = models.IntegerField()
    even_desc = models.CharField(max_length=120, blank=True, null=True)
    even_irrf = models.BooleanField(blank=True, null=True)
    even_inss = models.BooleanField(blank=True, null=True)
    even_safa = models.BooleanField(blank=True, null=True)
    even_fgts = models.BooleanField(blank=True, null=True)
    even_refl = models.BooleanField(blank=True, null=True)
    even_medi = models.BooleanField(blank=True, null=True)
    even_insa = models.BooleanField(blank=True, null=True)
    even_peri = models.BooleanField(blank=True, null=True)
    even_rais = models.BooleanField(blank=True, null=True)
    even_tipo = models.CharField(max_length=1)
    even_form = models.CharField(max_length=1)
    even_peva = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    even_dedu = models.BooleanField(blank=True, null=True)
    even_dere = models.CharField(max_length=2, blank=True, null=True)
    even_bpis = models.BooleanField(blank=True, null=True)
    even_naol = models.BooleanField(blank=True, null=True)
    even_notu = models.BooleanField(blank=True, null=True)
    even_gps = models.BooleanField(blank=True, null=True)
    even_cont = models.BooleanField(blank=True, null=True)
    even_bloq = models.BooleanField(blank=True, null=True)
    even_hera = models.BooleanField(blank=True, null=True)
    even_csra = models.BooleanField(blank=True, null=True)
    even_cara = models.BooleanField(blank=True, null=True)
    even_verb_resc = models.CharField(max_length=6, blank=True, null=True)
    even_plsa = models.BooleanField(blank=True, null=True)
    even_cnpj_plsa = models.CharField(max_length=14, blank=True, null=True)
    even_nome_plsa = models.CharField(max_length=150, blank=True, null=True)
    even_rans_plsa = models.CharField(max_length=6, blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.   
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.   
    even_empr = models.IntegerField()
    even_do_sist = models.BooleanField(blank=True, null=True)
    even_linh_clas = models.IntegerField(blank=True, null=True)
    even_base_hora_extr = models.BooleanField(blank=True, null=True)
    codinccp = models.IntegerField(blank=True, null=True)
    codincirrf = models.IntegerField(blank=True, null=True)
    codincfgts = models.IntegerField(blank=True, null=True)
    codincsind = models.IntegerField(blank=True, null=True)
    natrubr = models.CharField(max_length=6, blank=True, null=True)
    inivalid = models.CharField(max_length=6, blank=True, null=True)
    fimvalid = models.CharField(max_length=6, blank=True, null=True)
    even_dirf = models.CharField(max_length=6, blank=True, null=True)
    even_tipo_rubr = models.SmallIntegerField(blank=True, null=True)
    even_info_codi = models.BooleanField(blank=True, null=True)
    even_codi_esoc = models.CharField(max_length=6, blank=True, null=True)
    codinccprp = models.IntegerField(blank=True, null=True)
    codincpasep = models.IntegerField(blank=True, null=True)

    objects = BancoConsulta()   
    
    class Meta:
        managed = False
        db_table = 'eventos'
        unique_together = (('registro', 'even_empr', 'even_codi'),)

# Create your models here.
