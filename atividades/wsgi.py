from flask import Flask, request, jsonify
from flasgger import Swagger
import requests

def create_app():
    app = Flask(__name__)
    app.config["SWAGGER"] = {"title": "Atividades API", "uiversion": 3}
    Swagger(app)

    GERENCIAMENTO_URL = "http://gerenciamento:5001/api"

    atividades = []

    @app.post("/atividades")
    def criar_atividade():
        """
        Cria uma nova atividade (valida professor e turma via Gerenciamento)
        ---
        tags:
          - Atividades
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                titulo:
                  type: string
                descricao:
                  type: string
                professor_id:
                  type: integer
                turma_id:
                  type: integer
        responses:
          201:
            description: Atividade criada com sucesso
          400:
            description: Dados inválidos
        """
        data = request.get_json()
        titulo = data.get("titulo")
        descricao = data.get("descricao")
        professor_id = data.get("professor_id")
        turma_id = data.get("turma_id")

        if not all([titulo, professor_id, turma_id]):
            return jsonify({"error": "Campos obrigatórios: titulo, professor_id, turma_id"}), 400

        # 🔹 Valida o professor e a turma no Gerenciamento
        prof_resp = requests.get(f"{GERENCIAMENTO_URL}/professores/{professor_id}")
        turma_resp = requests.get(f"{GERENCIAMENTO_URL}/turmas/{turma_id}")

        if prof_resp.status_code != 200:
            return jsonify({"error": "Professor não encontrado"}), 400
        if turma_resp.status_code != 200:
            return jsonify({"error": "Turma não encontrada"}), 400

        atividade = {
            "id": len(atividades) + 1,
            "titulo": titulo,
            "descricao": descricao,
            "professor_id": professor_id,
            "turma_id": turma_id
        }
        atividades.append(atividade)
        return jsonify(atividade), 201

    @app.get("/atividades")
    def listar_atividades():
        """Lista todas as atividades"""
        return jsonify(atividades)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "atividades"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
