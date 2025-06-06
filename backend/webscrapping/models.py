from django.db import models

class Imoveis(models.Model):
    titulo = models.CharField(max_length=255, blank=True, null=True)
    preco = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    detalhes = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    link = models.CharField(unique=True, max_length=500, blank=True, null=True)
    tamanho = models.CharField(max_length=20, blank=True, null=True)
    quartos = models.CharField(max_length=20, blank=True, null=True)
    vagas = models.CharField(max_length=20, blank=True, null=True)
    suites = models.CharField(max_length=20, blank=True, null=True)
    plantas = models.CharField(max_length=20, blank=True, null=True)
    data_extracao = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'imoveis'
