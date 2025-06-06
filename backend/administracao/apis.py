from ninja import Router
from typing import List
from administracao.schemas import *
from administracao.views import *
from administracao.models import TbDisciplinas

router = Router()
@router.get(
    "/alunos",
    response=List[TbAlunosSchema],
    summary="Listar todos os alunos",
    description="Retorna todos os registros da tabela de alunos com informações completas de endereço e carro."
)
def pegar_alunos(request):
    return listar_alunos()


@router.get(
    "/consultar-alunos/{id}",
    response=TbAlunosSchema,
    summary="Consultar aluno por ID",
    description="Retorna os dados detalhados de um único aluno, incluindo suas relações com endereço e carro, com base no ID fornecido."
)
def get_aluno(request, id: int):
    return consultar_aluno_por_id(id)


@router.put(
    "/atualizar-alunos/{id}",
    response=TbAlunosSchema,
    summary="Atualizar dados de um aluno",
    description="Atualiza os dados de um aluno específico na base, com base no ID informado e nas novas informações fornecidas."
)
def put_aluno(request, id: int, data: TbAlunosSchemaIn):
    return atualizar_alunos_por_id(id, data)


@router.post(
    "/criar-aluno",
    response=TbAlunosSchema,
    summary="Criar um novo aluno",
    description="Cria um novo registro de aluno no banco de dados, com dados básicos e relações opcionais de endereço e carro."
)
def post_aluno(request, data: TbAlunosSchemaIn):
    return criar_novo_aluno(data)


@router.delete(
    "/deletar-aluno/{id}",
    response={204: None},
    summary="Deletar aluno por ID",
    description="Remove um aluno da base de dados de forma permanente, com base no ID fornecido."
)
def delete_aluno(request, id: int):
    deletar_aluno_por_id(id)
    return 204, None

@router.get("/enderecos", response=List[TbEnderecosSchema],
            summary="Listar todos os endereços",
            description="Retorna todos os endereços registrados no sistema.")
def get_enderecos(request):
    return listar_enderecos()

@router.get("/enderecos/{cep}", response=TbEnderecosSchema,
            summary="Consultar endereço por CEP",
            description="Retorna os dados completos de um endereço específico com base no CEP informado.")
def get_endereco(request, cep: str):
    return consultar_endereco(cep)

@router.post("/enderecos", response=TbEnderecosSchema,
             summary="Criar um novo endereço",
             description="Cria um novo endereço no sistema. O CEP deve ser válido e ainda não existente.")
def post_endereco(request, data: TbEnderecosSchemaIn):
    return criar_endereco(data)

@router.put("/enderecos/{cep}", response=TbEnderecosSchema,
            summary="Atualizar um endereço",
            description="Atualiza os dados de um endereço existente com base no CEP.")
def put_endereco(request, cep: str, data: TbEnderecosSchemaIn):
    return atualizar_endereco(cep, data)

@router.delete("/enderecos/{cep}", response={204: None},
               summary="Deletar um endereço",
               description="Remove um endereço do sistema com base no CEP fornecido.")
def delete_endereco(request, cep: str):
    deletar_endereco(cep)
    return 204, None

@router.get("/carros/{id}", response=TbCarrosSchema)
def get_carro(request, id: int):
    return consultar_carro(id)

@router.post("/carros", response=TbCarrosSchema)
def post_carro(request, data: TbCarrosSchemaIn):
    return criar_carro(data)

@router.get("/notas/aluno/{aluno_id}", response=List[TbNotasSchema],
            summary="Listar notas por aluno",
            description="Retorna todas as notas do aluno com as disciplinas.")
def get_notas_aluno(request, aluno_id: int):
    return listar_notas_por_aluno(aluno_id)

@router.get("/notas/{id}", response=TbNotasSchema)
def get_nota(request, id: int):
    return consultar_nota_por_id(id)

@router.post("/notas", response=TbNotasSchema)
def post_nota(request, data: TbNotasSchemaIn):
    return criar_nota(data)

@router.put("/notas/{id}", response=TbNotasSchema)
def put_nota(request, id: int, data: TbNotasSchemaIn):
    return atualizar_nota(id, data)

@router.delete("/notas/{id}", response={204: None})
def delete_nota(request, id: int):
    deletar_nota(id)
    return 204, None

@router.get("/disciplinas", response=List[TbDisciplinasSchema])
def get_disciplinas(request):
    return TbDisciplinas.objects.all()
