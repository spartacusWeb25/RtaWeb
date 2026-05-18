from django.db import models
from core.consultas import BancoConsulta

class Horarios(models.Model):
    registro = models.ForeignKey('Profissionais', models.DO_NOTHING, db_column='registro')
    hora_prof = models.IntegerField()
    hora_dia = models.IntegerField()
    hora_inic_1 = models.TimeField(blank=True, null=True)
    hora_fina_1 = models.TimeField(blank=True, null=True)
    hora_inic_2 = models.TimeField(blank=True, null=True)
    hora_fina_2 = models.TimeField(blank=True, null=True)
    hora_inic_3 = models.TimeField(blank=True, null=True)
    hora_fina_3 = models.TimeField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.   
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.   
    hora_data = models.DateField()

    objects = BancoConsulta()   

    class Meta:
        managed = False
        db_table = 'horarios'


# Create your models here.
