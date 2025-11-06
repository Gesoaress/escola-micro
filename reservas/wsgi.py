from flask import Flask, request, jsonify
from flasgger import Swagger
import requests

def create_app():
    app = Flask(__name__)
    app.config["SWAGGER"] = {"title": "Reservas API", "uiversion": 3}
    Swagger(app)

    GERENCIAMENTO_URL = "http://gerenciamento:5001/api"

    reservas = []

    @app.post("/reservas")
    def criar_reserva():
        """
        Cria uma nova reserva (valida aluno e turma via Gerenciamento)
        ---
        tags:
          - Reservas
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                aluno_id:
                  type: integer
                turma_id:
                  type: integer
        responses:
          201:
            description: Reserva criada
          400:
            description: Dados inválidos
        """
        data = request.get_json()
        aluno_id = data.get("aluno_id")
        turma_id = data.get("turma_id")

        # Validação de aluno
        aluno_resp = requests.get(f"{GERENCIAMENTO_URL}/alunos/{aluno_id}")
        turma_resp = requests.get(f"{GERENCIAMENTO_URL}/turmas/{turma_id}")

        if aluno_resp.status_code != 200:
            return jsonify({"error": "Aluno não encontrado"}), 400
        if turma_resp.status_code != 200:
            return jsonify({"error": "Turma não encontrada"}), 400

        reserva = {
            "id": len(reservas) + 1,
            "aluno_id": aluno_id,
            "turma_id": turma_id
        }
        reservas.append(reserva)
        return jsonify(reserva), 201

    @app.get("/reservas")
    def listar_reservas():
        """Lista todas as reservas"""
        return jsonify(reservas)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "reservas"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
