from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    db_path = os.path.join(os.path.dirname(__file__), "..", "gerenciamento.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Configuração basica do Swagger
    app.config['SWAGGER'] = {
        'title': 'Gerenciamento API',
        'uiversion': 3
    }
    Swagger(app)

    db.init_app(app)

    with app.app_context():
        from .models import Aluno, Professor, Turma
        db.create_all()

    #Importar e registra as rotas
    from .routes import bp 
    app.register_blueprint(bp, url_prefix='/api')
    
    return app

