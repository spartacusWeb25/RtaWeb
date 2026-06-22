from django.db import models
from core.utils import format_month_reference

class Tabelasalariominimo(models.Model):
    refe_sala_mini = models.CharField(primary_key=True, max_length=6)
    refe_sala_mini_fede = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    refe_sala_mini_esta = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    refe_sala_ref1 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    refe_sala_ref2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'tabelasalariominimo'

    @property
    def refe_sala_mini_formatada(self):
        return format_month_reference(self.refe_sala_mini)
