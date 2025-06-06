from django.db import models

# Create your models here.
# class TbAlunos(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     nome_aluno = models.CharField(max_length=255, blank = True, null = True)
#     email = models.CharField(max_length=255, blank = True, null = True)
#     cep = models.CharField(max_length=10, blank = False, null = True)
#     carro_id = models.IntegerField(blank = True, null = True)

# class Meta:
#     db_table = "tb_alunos"
#     managed = True

class TbAlunos(models.Model):
    nome_aluno = models.CharField(max_length=255)
    email = models.CharField(max_length=100, blank=True, null=True)
    cep = models.ForeignKey('TbEnderecos', models.DO_NOTHING, db_column='cep', blank=True, null=True)
    carro = models.ForeignKey('TbCarros', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_alunos'


class TbCarros(models.Model):
    fabricante = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    especificacao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_carros'


class TbDisciplinas(models.Model):
    nome_disciplina = models.CharField(max_length=255)
    carga = models.IntegerField()
    semestre = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'tb_disciplinas'


class TbEnderecos(models.Model):
    cep = models.CharField(primary_key=True, max_length=10)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    class Meta:
        managed = True
        db_table = 'tb_enderecos'


class TbNotas(models.Model):
    aluno = models.ForeignKey(TbAlunos, models.DO_NOTHING)
    disciplina = models.ForeignKey(TbDisciplinas, models.DO_NOTHING)
    nota = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_notas'
