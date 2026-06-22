from django.db import models



class Licencas(models.Model):
    lice_docu = models.CharField(max_length=20, primary_key=True)
    lice_nome = models.CharField(max_length=100, blank=True, null=True)
    lice_usua = models.IntegerField(blank=True, null=True)
    lice_empr = models.IntegerField(blank=True, null=True)
    lice_fili = models.IntegerField(blank=True, null=True)
    lice_bloq = models.BooleanField(default=False)
    lice_moti_bloq = models.CharField(max_length=255, blank=True, null=True)
    lice_data_bloq = models.DateField(blank=True, null=True)
    lice_sist = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "licencas"


class Usuarios(models.Model):
    id = models.IntegerField(primary_key=True)
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
        unique_together = (("registro", "id"),)


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
