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
                    "nome": {"type": "string"},
                    "email": {"type": "string"},
                    "area": {"type": "string"}
                },
                "required": ["nome", "email"]
            }
        }
    ],
    "responses": {201: {"description": "Professor criado com sucesso."}}
})
def create_professor():
    data = request.get_json() or {}
    nome = data.get("nome")
    email = data.get("email")
    area = data.get("area")

    if not nome or not email:
        return jsonify({"error": "Nome e email são obrigatórios"}), 400

    prof = Professor(nome=nome, email=email, area=area)
    db.session.add(prof)
    db.session.commit()
    return jsonify({"id": prof.id, "nome": prof.nome, "email": prof.email, "area": prof.area}), 201


# READ (GET ALL)
@bp.get("/professores")
@swag_from({
    "tags": ["Professores"],
    "description": "Lista todos os professores cadastrados.",
    "responses": {200: {"description": "Lista de professores."}}
})
def list_professores():
    professores = Professor.query.all()
    result = [{"id": p.id, "nome": p.nome, "email": p.email, "area": p.area} for p in professores]
    return jsonify(result)


# READ (GET BY ID)
@bp.get("/professores/<int:prof_id>")
@swag_from({
    "tags": ["Professores"],
    "description": "Busca um professor pelo ID.",
    "parameters": [{"name": "prof_id", "in": "path", "type": "integer", "required": True}],
    "responses": {200: {"description": "Professor encontrado."}, 404: {"description": "Professor não encontrado."}}
})
def get_professor(prof_id):
    prof = Professor.query.get(prof_id)
    if not prof:
        return jsonify({"error": "Professor não encontrado"}), 404
    return jsonify({"id": prof.id, "nome": prof.nome, "email": prof.email, "area": prof.area})


# UPDATE (PUT)
@bp.put("/professores/<int:prof_id>")
@swag_from({
    "tags": ["Professores"],
    "description": "Atualiza os dados de um professor.",
    "parameters": [
        {"name": "prof_id", "in": "path", "type": "integer", "required": True},
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "email": {"type": "string"},
                    "area": {"type": "string"}
                }
            }
        }
    ],
    "responses": {200: {"description": "Professor atualizado."}, 404: {"description": "Professor não encontrado."}}
})
def update_professor(prof_id):
    prof = Professor.query.get(prof_id)
    if not prof:
        return jsonify({"error": "Professor não encontrado"}), 404

    data = request.get_json() or {}
    prof.nome = data.get("nome", prof.nome)
    prof.email = data.get("email", prof.email)
    prof.area = data.get("area", prof.area)
    db.session.commit()
    return jsonify({"id": prof.id, "nome": prof.nome, "email": prof.email, "area": prof.area})


# DELETE
@bp.delete("/professores/<int:prof_id>")
@swag_from({
    "tags": ["Professores"],
    "description": "Remove um professor.",
    "parameters": [{"name": "prof_id", "in": "path", "type": "integer", "required": True}],
    "responses": {204: {"description": "Professor removido."}, 404: {"description": "Professor não encontrado."}}
})
def delete_professor(prof_id):
    prof = Professor.query.get(prof_id)
    if not prof:
        return jsonify({"error": "Professor não encontrado"}), 404

    db.session.delete(prof)
    db.session.commit()
    return "", 204



# -----------------------
# HEALTH CHECK
# -----------------------
@bp.get("/health")
def health():
    """Verifica se o serviço está ativo"""
    return {"status": "ok", "service": "gerenciamento"}
