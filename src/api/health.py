"""Endpoints de verificacion rapida de la API."""

from flask import Blueprint, jsonify
from src.extensions import db

bp = Blueprint("health", __name__, url_prefix="/health")


@bp.get("/")
def healthcheck() -> tuple[dict[str, str], int]:
    """Devuelve el estado actual de la aplicacion."""
    # TODO: agregar comprobaciones reales (db, cache, servicios externos).
    health_status = {"status": "ok"}

    try:
        # Comprobación de conexión a base de datos
        db.session.execute("SELECT 1")
        health_status["database"] = "ok"
    except Exception as e:
        health_status["database"] = f"error: {str(e)}"
        health_status["status"] = "error"

    # (Opcional) Simulación de otros servicios (cache, API externa)
    try:
        # Aquí se podría agregar verificación de Redis, servicios HTTP, etc.
        health_status["cache"] = "ok"
        health_status["external_services"] = "ok"
    except Exception as e:
        health_status["cache"] = f"error: {str(e)}"
        health_status["status"] = "error"

    # Devuelve respuesta JSON con código 200 si todo está bien, 500 si hay errores
    code = 200 if health_status["status"] == "ok" else 500
    return jsonify(health_status), code
