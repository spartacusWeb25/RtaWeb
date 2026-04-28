from django.db import models

# Create your models here.
class Calendariorh(models.Model):
    registro = models.CharField(max_length=14, primary_key=True)
    cale_cida = models.CharField(max_length=7)
    cale_refe = models.CharField(max_length=7)
    cale_data = models.DateField()
    cale_dia_desc = models.BooleanField(blank=True, null=True)
    _log_data = models.DateField(blank=True, null=True)
    _log_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calendariorh'


class Mensagensrh(models.Model):
    registro = models.CharField(max_length=14, primary_key=True)
    mens_empr = models.IntegerField()
    mens_mes = models.IntegerField()
    mens_linh_1 = models.CharField(max_length=100, blank=True, null=True)
    mens_linh_2 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mensagensrh'

