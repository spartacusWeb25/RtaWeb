from django.db import models



class LicencasRta(models.Model):
    lice_docu = models.CharField(max_length=20, primary_key=True)
    lice_banc = models.CharField(max_length=50)
    lice_senh = models.CharField(max_length=100)
    lice_prov = models.CharField(max_length=100, blank=True, null=True)
    lice_bloq = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "licencasrta"


class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    registro = models.CharField(max_length=20)
    usua_nome = models.CharField(max_length=100, blank=True, null=True)
    usua_login = models.CharField(max_length=50)
    usua_senh = models.CharField(max_length=100)
    usua_ativ = models.BooleanField(default=True)
    usua_grup = models.IntegerField(blank=True, null=True)
    super = models.BooleanField(default=False)
    usua_emai = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "usuarios"


class Logado(models.Model):
    registro = models.CharField(max_length=20, primary_key=True)
    usuario = models.IntegerField()
    ativo = models.BooleanField(default=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    hora_fim = models.TimeField(blank=True, null=True)
    obs = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "logado"