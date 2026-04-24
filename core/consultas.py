
from django.db import models

class BancoQuerySet(models.QuerySet):
    def do_banco(self, banco):
        if not banco:
            return self.none()
        return self.filter(registro=banco)


class BancoConsulta(models.Manager):
    def get_queryset(self):
        return BancoQuerySet(self.model, using=self._db)

    def do_banco(self, banco):
        return self.get_queryset().do_banco(banco)