from flask import Blueprint

bp = Blueprint("Gerenciamento", __name__)

@bp.get("/health")

def health():
    """
    Health Check 
    ---
    tags:
      - Sistema
    responses:
      200:
        description: Retorna o status do microserviço de gerenciamento
        examples:
            application/json: { "status": "ok", "service": "gerenciamento" }
    
    """
    return {"status": "ok", "service": "gerenciamento"}
