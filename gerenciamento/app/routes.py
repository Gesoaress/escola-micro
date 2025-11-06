from flask import Blueprint, request, jsonify
from flasgger.utils import swag_from
from . import db
from .models import Aluno

bp = Blueprint("gerenciamento", __name__)

# -----------------------
# CREATE (POST)
# -----------------------
@bp.post("/alunos")
@swag_from({
    "tags": ["Alunos"],
    "description": "Cria um novo aluno no sistema.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "email": {"type": "string"}
                },
                "required": ["nome", "email"]
            }
        }
    ],
    "responses": {
        201: {"description": "Aluno criado com sucesso."},
        400: {"description": "Erro de dados inválidos."}
    }
})
def create_aluno():
    data = request.get_json() or {}
    nome = data.get("nome")
    email = data.get("email")

    if not nome or not email:
        return jsonify({"error": "Nome e email são obrigatórios"}), 400

    aluno = Aluno(nome=nome, email=email)
    db.session.add(aluno)
    db.session.commit()
    return jsonify({"id": aluno.id, "nome": aluno.nome, "email": aluno.email}), 201


# -----------------------
# READ (GET ALL)
# -----------------------
@bp.get("/alunos")
@swag_from({
    "tags": ["Alunos"],
    "description": "Lista todos os alunos cadastrados.",
    "responses": {200: {"description": "Lista de alunos."}}
})
def get_alunos():
    alunos = Aluno.query.all()
    result = [{"id": a.id, "nome": a.nome, "email": a.email} for a in alunos]
    return jsonify(result)


# -----------------------
# READ (GET BY ID)
# -----------------------
@bp.get("/alunos/<int:aluno_id>")
@swag_from({
    "tags": ["Alunos"],
    "description": "Busca um aluno pelo ID.",
    "parameters": [{"name": "aluno_id", "in": "path", "type": "integer", "required": True}],
    "responses": {200: {"description": "Aluno encontrado."}, 404: {"description": "Aluno não encontrado."}}
})
def get_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404
    return jsonify({"id": aluno.id, "nome": aluno.nome, "email": aluno.email})


# -----------------------
# UPDATE (PUT)
# -----------------------
@bp.put("/alunos/<int:aluno_id>")
@swag_from({
    "tags": ["Alunos"],
    "description": "Atualiza dados de um aluno existente.",
    "parameters": [
        {"name": "aluno_id", "in": "path", "type": "integer", "required": True},
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "email": {"type": "string"}
                }
            }
        }
    ],
    "responses": {200: {"description": "Aluno atualizado."}, 404: {"description": "Aluno não encontrado."}}
})
def update_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    data = request.get_json() or {}
    aluno.nome = data.get("nome", aluno.nome)
    aluno.email = data.get("email", aluno.email)
    db.session.commit()

    return jsonify({"id": aluno.id, "nome": aluno.nome, "email": aluno.email})


# -----------------------
# DELETE
# -----------------------
@bp.delete("/alunos/<int:aluno_id>")
@swag_from({
    "tags": ["Alunos"],
    "description": "Remove um aluno do sistema.",
    "parameters": [{"name": "aluno_id", "in": "path", "type": "integer", "required": True}],
    "responses": {204: {"description": "Aluno removido."}, 404: {"description": "Aluno não encontrado."}}
})
def delete_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()
    return "", 204

# -----------------------
# CRUD DE PROFESSORES
# -----------------------

from .models import Professor

# CREATE (POST)
@bp.post("/professores")
@swag_from({
    "tags": ["Professores"],
    "description": "Cria um novo professor.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "example": "Carlos Almeida"},
                    "idade": {"type": "integer", "example": 40},
                    "email": {"type": "string", "example": "carlos.almeida@escola.com"},
                    "materia": {"type": "string", "example": "História"},
                    "observacoes": {"type": "string", "example": "Professor responsável pela turma do 7º ano"}
                },
                "required": ["nome", "idade", "email", "materia"]
            }
        }
    ],
    "responses": {
        201: {"description": "Professor criado com sucesso."},
        400: {"description": "Erro de dados inválidos."}
    }
})
def create_professor():
    data = request.get_json() or {}
    nome = data.get("nome")
    idade = data.get("idade")
    email = data.get("email")
    materia = data.get("materia")
    observacoes = data.get("observacoes")

    if not all([nome, idade, email, materia]):
        return jsonify({"error": "Campos 'nome', 'idade', 'email' e 'materia' são obrigatórios"}), 400

    # Evita duplicar e-mails
    if Professor.query.filter_by(email=email).first():
        return jsonify({"error": "Já existe um professor com este e-mail."}), 400

    prof = Professor(
        nome=nome,
        idade=idade,
        email=email,
        materia=materia,
        observacoes=observacoes
    )
    db.session.add(prof)
    db.session.commit()

    return jsonify({
        "id": prof.id,
        "nome": prof.nome,
        "idade": prof.idade,
        "email": prof.email,
        "materia": prof.materia,
        "observacoes": prof.observacoes
    }), 201


# READ (GET ALL)
@bp.get("/professores")
@swag_from({
    "tags": ["Professores"],
    "description": "Lista todos os professores cadastrados.",
    "responses": {200: {"description": "Lista de professores."}}
})
def list_professores():
    professores = Professor.query.all()
    result = [{
        "id": p.id,
        "nome": p.nome,
        "idade": p.idade,
        "email": p.email,
        "materia": p.materia,
        "observacoes": p.observacoes
    } for p in professores]
    return jsonify(result)


# READ (GET BY ID)
@bp.get("/professores/<int:prof_id>")
@swag_from({
    "tags": ["Professores"],
    "description": "Busca um professor pelo ID.",
    "parameters": [{"name": "prof_id", "in": "path", "type": "integer", "required": True}],
    "responses": {
        200: {"description": "Professor encontrado."},
        404: {"description": "Professor não encontrado."}
    }
})
def get_professor(prof_id):
    prof = Professor.query.get(prof_id)
    if not prof:
        return jsonify({"error": "Professor não encontrado"}), 404
    return jsonify({
        "id": prof.id,
        "nome": prof.nome,
        "idade": prof.idade,
        "email": prof.email,
        "materia": prof.materia,
        "observacoes": prof.observacoes
    })


# UPDATE (PUT)
@bp.put("/professores/<int:prof_id>")
@swag_from({
    "tags": ["Professores"],
    "description": "Atualiza os dados de um professor existente.",
    "parameters": [
        {"name": "prof_id", "in": "path", "type": "integer", "required": True},
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "idade": {"type": "integer"},
                    "email": {"type": "string"},
                    "materia": {"type": "string"},
                    "observacoes": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Professor atualizado."},
        404: {"description": "Professor não encontrado."}
    }
})
def update_professor(prof_id):
    prof = Professor.query.get(prof_id)
    if not prof:
        return jsonify({"error": "Professor não encontrado"}), 404

    data = request.get_json() or {}
    prof.nome = data.get("nome", prof.nome)
    prof.idade = data.get("idade", prof.idade)
    prof.email = data.get("email", prof.email)
    prof.materia = data.get("materia", prof.materia)
    prof.observacoes = data.get("observacoes", prof.observacoes)

    db.session.commit()
    return jsonify({
        "id": prof.id,
        "nome": prof.nome,
        "idade": prof.idade,
        "email": prof.email,
        "materia": prof.materia,
        "observacoes": prof.observacoes
    })


# DELETE
@bp.delete("/professores/<int:prof_id>")
@swag_from({
    "tags": ["Professores"],
    "description": "Remove um professor pelo ID.",
    "parameters": [{"name": "prof_id", "in": "path", "type": "integer", "required": True}],
    "responses": {
        204: {"description": "Professor removido."},
        404: {"description": "Professor não encontrado."}
    }
})
def delete_professor(prof_id):
    prof = Professor.query.get(prof_id)
    if not prof:
        return jsonify({"error": "Professor não encontrado"}), 404

    db.session.delete(prof)
    db.session.commit()
    return "", 204
# -----------------------
# CRUD DE TURMAS
# -----------------------

from .models import Turma

# CREATE (POST)
@bp.post("/turmas")
@swag_from({
    "tags": ["Turmas"],
    "description": "Cria uma nova turma.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "descricao": {"type": "string"}
                },
                "required": ["nome"]
            }
        }
    ],
    "responses": {201: {"description": "Turma criada com sucesso."}}
})
def create_turma():
    data = request.get_json() or {}
    nome = data.get("nome")
    descricao = data.get("descricao")

    if not nome:
        return jsonify({"error": "O campo nome é obrigatório"}), 400

    turma = Turma(nome=nome, descricao=descricao)
    db.session.add(turma)
    db.session.commit()
    return jsonify({"id": turma.id, "nome": turma.nome, "descricao": turma.descricao}), 201


# READ (GET ALL)
@bp.get("/turmas")
@swag_from({
    "tags": ["Turmas"],
    "description": "Lista todas as turmas cadastradas.",
    "responses": {200: {"description": "Lista de turmas."}}
})
def list_turmas():
    turmas = Turma.query.all()
    result = [{"id": t.id, "nome": t.nome, "descricao": t.descricao} for t in turmas]
    return jsonify(result)


# READ (GET BY ID)
@bp.get("/turmas/<int:turma_id>")
@swag_from({
    "tags": ["Turmas"],
    "description": "Busca uma turma pelo ID.",
    "parameters": [{"name": "turma_id", "in": "path", "type": "integer", "required": True}],
    "responses": {200: {"description": "Turma encontrada."}, 404: {"description": "Turma não encontrada."}}
})
def get_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({"error": "Turma não encontrada"}), 404
    return jsonify({"id": turma.id, "nome": turma.nome, "descricao": turma.descricao})


# UPDATE (PUT)
@bp.put("/turmas/<int:turma_id>")
@swag_from({
    "tags": ["Turmas"],
    "description": "Atualiza os dados de uma turma.",
    "parameters": [
        {"name": "turma_id", "in": "path", "type": "integer", "required": True},
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "descricao": {"type": "string"}
                }
            }
        }
    ],
    "responses": {200: {"description": "Turma atualizada."}, 404: {"description": "Turma não encontrada."}}
})
def update_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({"error": "Turma não encontrada"}), 404

    data = request.get_json() or {}
    turma.nome = data.get("nome", turma.nome)
    turma.descricao = data.get("descricao", turma.descricao)
    db.session.commit()

    return jsonify({"id": turma.id, "nome": turma.nome, "descricao": turma.descricao})


# DELETE
@bp.delete("/turmas/<int:turma_id>")
@swag_from({
    "tags": ["Turmas"],
    "description": "Remove uma turma.",
    "parameters": [{"name": "turma_id", "in": "path", "type": "integer", "required": True}],
    "responses": {204: {"description": "Turma removida."}, 404: {"description": "Turma não encontrada."}}
})
def delete_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({"error": "Turma não encontrada"}), 404

    db.session.delete(turma)
    db.session.commit()
    return "", 204




# -----------------------
# HEALTH CHECK
# -----------------------
@bp.get("/health")
def health():
    """Verifica se o serviço está ativo"""
    return {"status": "ok", "service": "gerenciamento"}
