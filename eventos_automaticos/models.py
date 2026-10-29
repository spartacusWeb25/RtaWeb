from django.db import models


class EventosAutomaticos(models.Model):
    registro = models.CharField(primary_key=True, max_length=14)
    even_empr = models.IntegerField()
    even_fili = models.IntegerField()
    even_tipo_calculo = models.CharField(max_length=2)
    even_codi = models.IntegerField()
    log_data = models.DateField(db_column="_log_data", blank=True, null=True)
    log_hora = models.TimeField(db_column="_log_time", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "eventos_automaticos"
        unique_together = (
            ("registro", "even_empr", "even_fili", "even_tipo_calculo", "even_codi"),
        )
