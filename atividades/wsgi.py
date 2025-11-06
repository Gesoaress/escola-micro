from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config["SWAGGER"] = {"title": "Atividades API", "uiversion": 3}
    Swagger(app)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "atividades"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
