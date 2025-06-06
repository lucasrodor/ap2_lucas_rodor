from django.shortcuts import get_object_or_404
from administracao.models import TbAlunos, TbEnderecos, TbCarros, TbNotas, TbDisciplinas
from administracao.schemas import TbAlunosSchemaIn, TbEnderecosSchemaIn, TbCarrosSchemaIn, TbNotasSchemaIn


def listar_alunos():
    return TbAlunos.objects.select_related("cep", "carro").all()


def consultar_aluno_por_id(aluno_id: int):
    return TbAlunos.objects.select_related("cep", "carro").get(id=aluno_id)


def atualizar_alunos_por_id(aluno_id: int, data: TbAlunosSchemaIn):
    aluno = get_object_or_404(TbAlunos, id=aluno_id)
    aluno.nome_aluno = data.nome_aluno
    aluno.email = data.email

    aluno.cep = TbEnderecos.objects.get(pk=data.cep) if data.cep else None
    aluno.carro = TbCarros.objects.get(pk=data.carro) if data.carro else None

    aluno.save()
    return aluno


def criar_novo_aluno(data: TbAlunosSchemaIn):
    aluno = TbAlunos(
        nome_aluno=data.nome_aluno,
        email=data.email,
        cep=TbEnderecos.objects.get(pk=data.cep) if data.cep else None,
        carro=TbCarros.objects.get(pk=data.carro) if data.carro else None
    )
    aluno.save()
    return aluno


def deletar_aluno_por_id(aluno_id: int):
    aluno = get_object_or_404(TbAlunos, id=aluno_id)
    aluno.delete()
    return

def validar_cep(cep: str):
    if not cep:
        return None
    cep_limpo = cep.strip().replace("-", "").replace(".", "").replace(" ", "")
    return cep_limpo if cep_limpo.isdigit() and len(cep_limpo) == 8 else None

def verificar_cep_existe(cep: str):
    return TbEnderecos.objects.filter(cep=cep).exists()

def listar_enderecos():
    return TbEnderecos.objects.all()

def consultar_endereco(cep: str):
    return get_object_or_404(TbEnderecos, cep=cep)

def criar_endereco(data: TbEnderecosSchemaIn):
    cep_validado = validar_cep(data.cep)
    if not cep_validado or verificar_cep_existe(cep_validado):
        raise ValueError("CEP inválido ou já existente")
    endereco = TbEnderecos(
        cep=cep_validado,
        endereco=data.endereco,
        cidade=data.cidade,
        estado=data.estado
    )
    endereco.save()
    return endereco

def atualizar_endereco(cep: str, data: TbEnderecosSchemaIn):
    endereco = get_object_or_404(TbEnderecos, cep=cep)
    endereco.endereco = data.endereco
    endereco.cidade = data.cidade
    endereco.estado = data.estado
    endereco.save()
    return endereco

def deletar_endereco(cep: str):
    endereco = get_object_or_404(TbEnderecos, cep=cep)
    endereco.delete()

def consultar_carro(carro_id: int):
    return get_object_or_404(TbCarros, pk=carro_id)

def criar_carro(data: TbCarrosSchemaIn):
    carro = TbCarros(
        fabricante=data.fabricante,
        modelo=data.modelo,
        especificacao=data.especificacao
    )
    carro.save()
    return carro

def listar_notas_por_aluno(aluno_id: int):
    return TbNotas.objects.select_related("disciplina", "aluno").filter(aluno_id=aluno_id)

def consultar_nota_por_id(nota_id: int):
    return get_object_or_404(TbNotas, id=nota_id)

def criar_nota(data: TbNotasSchemaIn):
    nota = TbNotas(
        aluno_id=data.aluno,
        disciplina_id=data.disciplina,
        nota=data.nota
    )
    nota.save()
    return nota

def atualizar_nota(nota_id: int, data: TbNotasSchemaIn):
    nota = get_object_or_404(TbNotas, id=nota_id)
    nota.nota = data.nota
    nota.save()
    return nota

def deletar_nota(nota_id: int):
    nota = get_object_or_404(TbNotas, id=nota_id)
    nota.delete()

