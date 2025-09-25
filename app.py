from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Academia, Professor, Aluno
from logger import logger
from schemas import *
from flask_cors import CORS
from flask import request


from flask import jsonify
from sqlalchemy.orm import joinedload

from schemas import AcademiaCreate, AcademiaViewSchema, AcademiaBuscaSchema, ProfessorViewSchema, ProfessorBuscaSchema, ProfessorDelSchema, ListagemProfessoresSchema, AlunoCreate, AlunoViewSchema, AlunoBuscaSchema, AlunoDelSchema, ListagemAlunosSchema

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Home", description="Ponto de entrada da API. Pode incluir informações gerais, status ou documentação.")
academia_tag = Tag(name="Academia", description="Operações relacionadas à gestão de academias, como criação, listagem e atualização.")
professor_tag = Tag(name="Professor", description="Gerenciamento de professores vinculados às academias, incluindo cadastro e status de atividade")
aluno_tag = Tag(name="Aluno", description="Cadastro, listagem e busca de alunos, com suporte a visualizações personalizadas via views.")

@app.get('/', tags=[home_tag])
def home():
    """Esta é a rota principal da aplicação. Ao ser acessada, ela realiza um redirecionamento automático para a interface de documentação interativa da API, disponível em /openapi.

    Essa funcionalidade tem como objetivo facilitar o acesso dos usuários à documentação dos endpoints, permitindo testes e visualização dos dados esperados em cada requisição.
    """
    return redirect('/openapi')

@app.post('/academia', tags=[academia_tag],
          responses={"200": AcademiaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_academia(form: AcademiaCreate):
    """Adiciona uma nova Academia à base de dados

    Retorna uma representação da academia cadastrada.
    """
    academia = Academia(
        nome=form.nome,
        responsavel=form.responsavel
    )
    logger.debug(f"Adicionando academia de nome: '{academia.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando academia
        session.add(academia)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionada academia de nome: '{academia.nome}'")
        return apresenta_academia(academia), 200

    except IntegrityError as e:
        error_msg = "Academia de mesmo nome já salva na base :/"
        logger.warning(f"Erro ao adicionar academia '{academia.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar nova academia :/"
        logger.warning(f"Erro ao adicionar academia '{academia.nome}', {error_msg}")
        return {"message": error_msg}, 400
    




@app.get('/academias', tags=[academia_tag],
        responses={"200": AcademiaRead, "404": ErrorSchema})
def get_academias():
    """Faz a busca por todas as Academias cadastradas

    Retorna uma representação da listagem de academias.
    """
    logger.debug("Coletando academias")
    session = Session()
    academias = session.query(Academia).all()

    if not academias:
        return {"academias": []}, 200
    else:
        logger.debug(f"{len(academias)} academias encontradas")
        return apresenta_academias(academias), 200


@app.get('/academia', tags=[academia_tag],
         responses={"200": AcademiaViewSchema, "404": ErrorSchema})
def get_academia(query: AcademiaCreate):
    """Faz a busca por uma Academia a partir do nome

    Retorna uma representação da academia cadastrada.
    """
    nome = query.nome
    logger.debug(f"Buscando academia com nome: {nome}")
    session = Session()
    academia = session.query(Academia).filter(Academia.nome == nome).first()

    if not academia:
        error_msg = "Academia não encontrada na base :/"
        logger.warning(f"Erro ao buscar academia '{nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Academia encontrada: '{academia.nome}'")
        return apresenta_academia(academia), 200


@app.delete('/academia', tags=[academia_tag],
            responses={"200": AcademiaViewSchema, "404": ErrorSchema})
def del_academia(query: AcademiaBuscaSchema):
    """Deleta uma Academia a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    nome = unquote(unquote(query.nome))
    logger.debug(f"Deletando academia com nome: {nome}")
    session = Session()
    count = session.query(Academia).filter(Academia.nome == nome).delete()
    session.commit()

    if count:
        logger.debug(f"Academia deletada: {nome}")
        return {"message": "Academia removida", "id": nome}
    else:
        error_msg = "Academia não encontrada na base :/"
        logger.warning(f"Erro ao deletar academia '{nome}', {error_msg}")
        return {"message": error_msg}, 404
    

"""Funções de academia"""

def apresenta_academia(academia):
    """Retorna uma representação da academia única"""
    return {
        "id": academia.id,
        "nome": academia.nome,
        "responsavel": academia.responsavel,
        "data_insercao": str(academia.data_insercao)
    }

def apresenta_academias(academias):
    """Retorna uma lista de representações de academias"""
    return {
        "academias": [
            apresenta_academia(acad) for acad in academias
        ]
    }


@app.post('/professor', tags=[professor_tag],
          responses={"200": ProfessorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_professor():
    """Adiciona um novo Professor à base de dados

    Retorna uma representação do professor cadastrado.
    """
    try:
        nome = request.form.get('nome')
        academia_id = request.form.get('academia_id')
        ativo = request.form.get('ativo', 'true')  # default para ativo

        if not nome or not academia_id:
            return {"message": "Campos obrigatórios ausentes"}, 400

        professor = Professor(
            nome=nome,
            academia_id=int(academia_id),
            ativo=(ativo.lower() == 'true')
        )

        session = Session()
        session.add(professor)
        session.commit()
        logger.debug(f"Adicionado professor de nome: '{professor.nome}'")
        return apresenta_professor(professor), 200

    except IntegrityError:
        session.rollback()
        error_msg = "Professor de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar professor '{nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()
        error_msg = f"Não foi possível salvar novo professor: {str(e)}"
        logger.warning(f"Erro ao adicionar professor '{nome}', {error_msg}")
        return {"message": error_msg}, 400




@app.get('/professores', tags=[professor_tag],
         responses={"200": ListagemProfessoresSchema, "404": ErrorSchema})
def get_professores():
    """Faz a busca por todos os Professores cadastrados

    Retorna uma representação da listagem de professores.
    """
    logger.debug("Coletando professores")
    session = Session()
    professores = session.query(Professor).options(joinedload(Professor.academia)).all()

    if not professores:
        return {"professores": []}, 200

    resultado = []
    for prof in professores:
        resultado.append({
            "id": prof.id,
            "nome": prof.nome,
            "academia_id": prof.academia_id,
            "academia_nome": prof.academia.nome if prof.academia else "-",
            "data_insercao": prof.data_insercao.strftime("%d/%m/%Y %H:%M"),
            "ativo": prof.ativo
        })

    logger.debug(f"{len(resultado)} professores encontrados")
    return {"professores": resultado}, 200




@app.get('/professor', tags=[professor_tag],
         responses={"200": ProfessorViewSchema, "404": ErrorSchema})
def get_professor(query: ProfessorBuscaSchema):
    """Faz a busca por um Professor a partir do nome

    Retorna uma representação do professor cadastrado.
    """
    nome = query.nome
    logger.debug(f"Buscando professor com nome: {nome}")
    session = Session()
    professor = session.query(Professor).filter(Professor.nome == nome).first()

    if not professor:
        error_msg = "Professor não encontrado na base :/"
        logger.warning(f"Erro ao buscar professor '{nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Professor encontrado: '{professor.nome}'")
        return apresenta_professor(professor), 200


@app.delete('/professor', tags=[professor_tag],
            responses={"200": ProfessorDelSchema, "404": ErrorSchema})
def del_professor(query: ProfessorBuscaSchema):
    """Deleta um Professor a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    nome = unquote(unquote(query.nome))
    logger.debug(f"Deletando professor com nome: {nome}")
    session = Session()
    count = session.query(Professor).filter(Professor.nome == nome).delete()
    session.commit()

    if count:
        logger.debug(f"Professor deletado: {nome}")
        return {"message": "Professor removido", "id": nome}
    else:
        error_msg = "Professor não encontrado na base :/"
        logger.warning(f"Erro ao deletar professor '{nome}', {error_msg}")
        return {"message": error_msg}, 


"""Funções de professor"""

def apresenta_professor(professor):
    """Retorna uma representação do professor único"""
    return {
        "id": professor.id,
        "nome": professor.nome,
        "academia_id": professor.academia_id,
        "ativo": professor.ativo,
        "data_insercao": str(professor.data_insercao)
    }

def apresenta_professores(professores):
    """Retorna uma lista de representações de professores"""
    return {
        "professores": [
            apresenta_professor(prof) for prof in professores
        ]
    }


@app.post('/aluno', tags=[aluno_tag],
          responses={"200": AlunoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_aluno():
    """Adiciona um novo Aluno à base de dados

    Retorna uma representação do aluno cadastrado.
    """
    try:
        nome = request.form.get('nome')
        academia_id = request.form.get('academia_id')
        professor_id = request.form.get('professor_id')  # pode ser vazio
        ativo = request.form.get('ativo', 'true')

        if not nome or not academia_id:
            return {"message": "Campos obrigatórios 'nome' e 'academia_id' são necessários."}, 400

        aluno = Aluno(
            nome=nome,
            academia_id=int(academia_id),
            professor_id=int(professor_id) if professor_id else None,
            ativo=(ativo.lower() == 'true')
        )

        session = Session()
        session.add(aluno)
        session.commit()
        logger.debug(f"Adicionado aluno de nome: '{aluno.nome}'")
        return apresenta_aluno(aluno), 200

    except IntegrityError:
        session.rollback()
        error_msg = "Aluno de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar aluno '{nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()
        error_msg = f"Não foi possível salvar novo aluno: {str(e)}"
        logger.warning(f"Erro ao adicionar aluno '{nome}', {error_msg}")
        return {"message": error_msg}, 400




@app.get('/alunos', tags=[aluno_tag],
         responses={"200": ListagemAlunosSchema, "404": ErrorSchema})
def get_alunos():
    """Faz a busca por todos os Alunos cadastrados

    Retorna uma representação da listagem de alunos.
    """
    session = Session()
    alunos = session.query(Aluno).options(
        joinedload(Aluno.professor),
        joinedload(Aluno.academia)
    ).all()

    resultado = []
    for aluno in alunos:
        resultado.append({
            "id": aluno.id,
            "nome": aluno.nome,
            "professor_nome": aluno.professor.nome if aluno.professor else "-",
            "academia_nome": aluno.academia.nome if aluno.academia else "-",
            "data_inscricao": aluno.data_inscricao.strftime("%d/%m/%Y %H:%M"),
            "ativo": aluno.ativo
        })

    return {"alunos": resultado}, 200


@app.get('/aluno', tags=[aluno_tag],
         responses={"200": AlunoViewSchema, "404": ErrorSchema})
def get_aluno(query: AlunoBuscaSchema):
    """Faz a busca por um Aluno a partir do nome

    Retorna uma representação do aluno cadastrado.
    """
    nome = query.nome
    logger.debug(f"Buscando aluno com nome: {nome}")
    session = Session()
    aluno = session.query(Aluno).filter(Aluno.nome == nome).first()

    if not aluno:
        error_msg = "Aluno não encontrado na base :/"
        logger.warning(f"Erro ao buscar aluno '{nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Aluno encontrado: '{aluno.nome}'")
        return apresenta_aluno(aluno), 200


@app.delete('/aluno', tags=[aluno_tag],
            responses={"200": AlunoDelSchema, "404": ErrorSchema})
def del_aluno(query: AlunoBuscaSchema):
    """Deleta um Aluno a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    nome = unquote(unquote(query.nome))
    logger.debug(f"Deletando aluno com nome: {nome}")
    session = Session()
    count = session.query(Aluno).filter(Aluno.nome == nome).delete()
    session.commit()

    if count:
        logger.debug(f"Aluno deletado: {nome}")
        return {"message": "Aluno removido", "id": nome}
    else:
        error_msg = "Aluno não encontrado na base :/"
        logger.warning(f"Erro ao deletar aluno '{nome}', {error_msg}")
        return {"message": error_msg}, 404
    

"""Funções de aluno"""

def apresenta_aluno(aluno):
    """Retorna uma representação do aluno único"""
    return {
        "id": aluno.id,
        "nome": aluno.nome,
        "professor_id": aluno.professor_id,
        "academia_id": aluno.academia_id,
        "ativo": aluno.ativo,
        "data_inscricao": str(aluno.data_inscricao)
    }

def apresenta_alunos(alunos):
    """Retorna uma lista de representações de alunos"""
    return {
        "alunos": [
            apresenta_aluno(aluno) for aluno in alunos
        ]
    }