from django.db import models
from core.consultas import BancoConsulta
from funcionarios.models import Funcionarios


class Folhamensal(models.Model):  # <-- resolve o problema de chave primária não sendo auto-incrementada
    registro = models.ForeignKey(
        Funcionarios,
        models.DO_NOTHING,
        db_column='registro', 
        primary_key=True
     
    )
    fome_even = models.IntegerField()
    fome_base = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_perc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_faix = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_desa = models.IntegerField(blank=True, null=True)
    fome_deir = models.IntegerField(blank=True, null=True)
    fome_tipo = models.CharField(max_length=1, blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True
    )
    fome_empr = models.IntegerField()
    fome_fili = models.IntegerField()
    fome_func = models.IntegerField()
    fome_refe = models.CharField(max_length=6)
    fome_even = models.IntegerField()
    fome_base = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_perc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    fome_valo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_faix = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fome_desa = models.IntegerField(blank=True, null=True)
    fome_deir = models.IntegerField(blank=True, null=True)
    fome_tipo = models.CharField(max_length=1, blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)
    fome_tipo_base = models.CharField(max_length=5, blank=True, null=True)
    fome_orde_clas = models.CharField(max_length=10, blank=True, null=True)
    fome_data_paga = models.DateField(blank=True, null=True)
    fome_refe_prox_paga = models.CharField(max_length=6, blank=True, null=True)
    fome_depa = models.IntegerField(blank=True, null=True)
    fome_seto = models.IntegerField(blank=True, null=True)

    objects = BancoConsulta()

    class Meta:
        managed = False
        db_table = 'folhamensal'
        unique_together = (
            ('registro', 'fome_empr', 'fome_fili', 'fome_func', 'fome_refe', 'fome_even'),
        )