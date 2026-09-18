from django.db import models


class PlanoCargos(models.Model):
    registro = models.CharField(primary_key=True, max_length=14, db_column="registro")

    class Meta:
        managed = False
        app_label = "planoscargos"
        db_table = "planoscargos"

    def save(self, *args, **kwargs):
        raise NotImplementedError("Implementar no futuro")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("Implementar no futuro")
