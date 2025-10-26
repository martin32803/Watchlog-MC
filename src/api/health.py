from flask import Blueprint, jsonify
from src.extensions import db
from sqlalchemy import text  # ✅ importa text

bp = Blueprint("health", __name__, url_prefix="/health")


@bp.get("/")
def healthcheck() -> tuple[dict[str, str], int]:
    """Devuelve el estado actual de la aplicacion."""
    health_status = {"status": "ok"}

    try:
        # usa text("SELECT 1") para compatibilidad con SQLAlchemy 2.x
        db.session.execute(text("SELECT 1"))
        health_status["database"] = "ok"
    except Exception as e:
        health_status["database"] = f"error: {str(e)}"
        health_status["status"] = "error"

    # Simulaciones de otros servicios
    health_status["cache"] = "ok"
    health_status["external_services"] = "ok"

    code = 200 if health_status["status"] == "ok" else 500
    return jsonify(health_status), code
