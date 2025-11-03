from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    # Configuração basica do Swagger
    app.config['SWAGGER'] = {
        'title': 'Gerenciamento API',
        'uiversion': 3
    }
    Swagger(app)

    #Importar e registra as rotas
    from .routes import bp 
    app.register_blueprint(bp, url_prefix='/api')
    
    return app

