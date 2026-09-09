from django.db import models
from core.consultas import BancoConsulta


class Dependentescontr(models.Model):
    registro = models.CharField(max_length=14, primary_key=True)
    depecontr_empr = models.IntegerField()
    depecontr_fili = models.IntegerField()
    depecontr_contr = models.IntegerField()
    depecontr_codi = models.IntegerField()

    depecontr_nome = models.CharField(max_length=200, blank=True, null=True)
    depecontr_nascimento = models.DateField(blank=True, null=True)
    depecontr_cpf = models.CharField(max_length=14, blank=True, null=True)
    depecontr_matricula = models.CharField(max_length=30, blank=True, null=True)
    depecontr_local_nascimento = models.CharField(max_length=60, blank=True, null=True)
    depecontr_cidade_codigo = models.IntegerField(blank=True, null=True)
    depecontr_cidade = models.CharField(max_length=60, blank=True, null=True)
    depecontr_cartorio = models.CharField(max_length=120, blank=True, null=True)
    depecontr_numero_registro = models.CharField(max_length=20, blank=True, null=True)
    depecontr_numero_livro = models.CharField(max_length=20, blank=True, null=True)
    depecontr_numero_folha = models.CharField(max_length=20, blank=True, null=True)
    depecontr_data_entrega = models.DateField(blank=True, null=True)
    depecontr_tipo_dependencia = models.IntegerField(blank=True, null=True)
    depecontr_data_baixa = models.DateField(blank=True, null=True)
    depecontr_ir_ate = models.CharField(max_length=7, blank=True, null=True)
    depecontr_tipo_dependente = models.IntegerField(blank=True, null=True)
    depecontr_invalido = models.BooleanField(default=False, blank=True, null=True)
    depecontr_observacoes = models.TextField(blank=True, null=True)
    depecontr_grau_parentesco = models.IntegerField(blank=True, null=True)
    depecontr_pensao_alimenticia_valor = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    depecontr_pensao_alimenticia_percentual = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    depecontr_dependente_irrf = models.BooleanField(default=False, blank=True, null=True)
    depecontr_dependente_salario_familia = models.BooleanField(default=False, blank=True, null=True)
    depecontr_rg = models.CharField(max_length=20, blank=True, null=True)
    depecontr_orgao_emissor_rg = models.CharField(max_length=20, blank=True, null=True)
    depecontr_uf_rg = models.CharField(max_length=2, blank=True, null=True)
    depecontr_emissao_rg = models.DateField(blank=True, null=True)
    depecontr_certidao_nascimento = models.CharField(max_length=30, blank=True, null=True)
    depecontr_desc_dependencia = models.CharField(max_length=255, blank=True, null=True)

    objects = BancoConsulta()

    class Meta:
        managed = False
        db_table = "dependentescontr"
        unique_together = (
            ("registro", "depecontr_empr", "depecontr_fili", "depecontr_contr", "depecontr_codi"),
        )

    def __str__(self):
        return self.depecontr_nome or f"Dependente #{self.depecontr_codi}"

    def save(self, *args, **kwargs):
        using = kwargs.get("using") or "default"
        qs = Dependentescontr.objects.using(using).filter(
            registro=self.registro,
            depecontr_empr=self.depecontr_empr,
            depecontr_fili=self.depecontr_fili,
            depecontr_contr=self.depecontr_contr,
            depecontr_codi=self.depecontr_codi,
        )
        if qs.exists():
            dados = {}
            for field in self._meta.get_fields():
                if field.primary_key:
                    continue
                if field.name in ("registro", "depecontr_empr", "depecontr_fili", "depecontr_contr", "depecontr_codi"):
                    continue
                try:
                    dados[field.name] = getattr(self, field.name)
                except Exception:
                    pass
            qs.update(**dados)
            return self
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        using = kwargs.get("using") or "default"
        Dependentescontr.objects.using(using).filter(
            registro=self.registro,
            depecontr_empr=self.depecontr_empr,
            depecontr_fili=self.depecontr_fili,
            depecontr_contr=self.depecontr_contr,
            depecontr_codi=self.depecontr_codi,
        ).delete()
