from django.db import models
from core.consultas import BancoConsulta

class Dadosrescisao(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    dare_empr = models.IntegerField()
    dare_func = models.IntegerField()
    dare_data_avis = models.DateField(blank=True, null=True)
    dare_demi = models.DateField(blank=True, null=True)
    dare_dapa = models.DateField(blank=True, null=True)
    dare_tipo = models.IntegerField(blank=True, null=True)
    dare_sasa = models.BooleanField(blank=True, null=True)
    dare_avin = models.BooleanField(blank=True, null=True)
    dare_avpa = models.BooleanField(blank=True, null=True)
    dare_feri = models.BooleanField(blank=True, null=True)
    dare_de13 = models.BooleanField(blank=True, null=True)
    dare_fgmr = models.BooleanField(blank=True, null=True)
    dare_fgma = models.BooleanField(blank=True, null=True)
    dare_fgmu = models.BooleanField(blank=True, null=True)
    dare_grfc = models.BooleanField(blank=True, null=True)
    dare_mult = models.IntegerField(blank=True, null=True)
    dare_avis = models.IntegerField(blank=True, null=True)
    dare_perc_avis = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dare_perc_mult = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dare_sald_fgts = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    dare_chav_iden = models.CharField(max_length=255, blank=True, null=True)
    dare_obse = models.TextField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.   
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.   
    dare_refe = models.CharField(max_length=6, blank=True, null=True)
    dare_feri_prop = models.BooleanField(blank=True, null=True)
    dare_tipo_avis = models.IntegerField(blank=True, null=True)
    dare_moti_desl = models.CharField(max_length=2, blank=True, null=True)
    dare_inde_empr = models.BooleanField(blank=True, null=True)
    dare_term_avis = models.DateField(blank=True, null=True)
    dare_pens_alim = models.IntegerField(blank=True, null=True)
    dare_perc_pens_alim = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dare_valo_pens_alim = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    dare_cert_obit = models.CharField(max_length=32, blank=True, null=True)
    dare_cump_avis_prev = models.IntegerField(blank=True, null=True)
    dare_naopagar112avos = models.BooleanField(blank=True, null=True)
    dare_func_trans_empr = models.BooleanField(blank=True, null=True)
    dare_func_trans_empr_tpinsc = models.IntegerField(blank=True, null=True)
    dare_func_trans_empr_nrinsc = models.CharField(max_length=14, blank=True, null=True)

    objects = BancoConsulta()   

    class Meta:
        managed = False
        db_table = 'dadosrescisao'
        unique_together = (('registro', 'dare_empr', 'dare_func'),)
