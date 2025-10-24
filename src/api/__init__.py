"""Registro centralizado de blueprints."""

from flask import Flask


def register_api_blueprints(app: Flask) -> None:
    """Agrega todos los blueprints disponibles a la aplicacion."""
    from .health import bp as health_bp
    from .movies import bp as movies_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(movies_bp)


__all__ = ["register_api_blueprints"]
