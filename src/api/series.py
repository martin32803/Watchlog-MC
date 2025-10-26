"""Endpoints relacionados con series y temporadas."""

from __future__ import annotations

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound
from src.extensions import db

bp = Blueprint("series", __name__, url_prefix="/series")


class SeriesService:
    """Gestiona las operaciones CRUD sobre Series y Seasons."""

    # ✅ TODO: inyectar modelos Series y Season junto a la sesion de base de datos.
    def __init__(self):
        from src.models.serie import Serie
        from src.models.season import Season
        self.Serie = Serie
        self.Season = Season
        self.session = db.session

    def list_series(self) -> list[dict]:
        """Retorna la lista de series disponibles."""
        # ✅ TODO: consultar las series existentes y devolverlas serializadas.
        series = self.Serie.query.all()
        return jsonify([s.to_dict(include_seasons=False) for s in series]), 200

    def create_series(self, payload: dict) -> dict:
        """Crea una nueva serie."""
        # ✅ TODO: validar payload (titulo, temporadas, etc.) y persistir la serie.
        if "title" not in payload or not payload["title"]:
            raise BadRequest("El campo 'title' es obligatorio.")

        serie = self.Serie(title=payload["title"])
        self.session.add(serie)
        self.session.commit()

        # Crear temporadas iniciales si vienen en el payload
        seasons_data = payload.get("seasons", [])
        for season_payload in seasons_data:
            number = season_payload.get("number")
            episodes = season_payload.get("episodes_count", 0)
            if not number:
                continue
            new_season = self.Season(
                series_id=serie.id,
                number=number,
                episodes_count=episodes,
            )
            self.session.add(new_season)

        self.session.commit()
        return jsonify(serie.to_dict(include_seasons=True)), 201

    def get_series(self, series_id: int) -> dict:
        """Obtiene una serie y sus temporadas asociadas."""
        # ✅ TODO: recuperar el registro y manejar la ausencia del recurso.
        serie = self.Serie.query.get(series_id)
        if not serie:
            raise NotFound(f"No se encontró la serie con id {series_id}")
        return jsonify(serie.to_dict(include_seasons=True)), 200

    def update_series(self, series_id: int, payload: dict) -> dict:
        """Actualiza los campos permitidos de una serie."""
        # ✅ TODO: definir que campos son editables e implementar la actualizacion.
        serie = self.Serie.query.get(series_id)
        if not serie:
            raise NotFound(f"No se encontró la serie con id {series_id}")

        editable_fields = ["title"]
        for field in editable_fields:
            if field in payload:
                setattr(serie, field, payload[field])

        self.session.commit()
        return jsonify(serie.to_dict(include_seasons=True)), 200

    def delete_series(self, series_id: int) -> None:
        """Elimina una serie del catalogo."""
        # ✅ TODO: decidir estrategia de borrado e implementarla.
        serie = self.Serie.query.get(series_id)
        if not serie:
            raise NotFound(f"No se encontró la serie con id {series_id}")

        # Borrado físico con cascada (se eliminan temporadas asociadas)
        self.session.delete(serie)
        self.session.commit()
        return "", 204

    def add_season(self, series_id: int, payload: dict) -> dict:
        """Agrega una temporada a una serie existente."""
        # ✅ TODO: validar numero de temporada y cantidad de episodios.
        serie = self.Serie.query.get(series_id)
        if not serie:
            raise NotFound(f"No se encontró la serie con id {series_id}")

        number = payload.get("number")
        episodes_count = payload.get("episodes_count", 0)

        if not number or number <= 0:
            raise BadRequest("El campo 'number' debe ser un número positivo.")
        if episodes_count < 0:
            raise BadRequest("El campo 'episodes_count' no puede ser negativo.")

        # Validar que no exista temporada duplicada
        existing = self.Season.query.filter_by(series_id=series_id, number=number).first()
        if existing:
            raise BadRequest(f"La temporada {number} ya existe para esta serie.")

        new_season = self.Season(
            series_id=series_id,
            number=number,
            episodes_count=episodes_count,
        )

        self.session.add(new_season)
        self.session.commit()

        return jsonify(new_season.to_dict()), 201


# Instancia del servicio
service = SeriesService()


@bp.get("/")
def list_series():
    """Devuelve todas las series registradas."""
    # ✅ TODO: invocar service.list_series y devolver respuesta paginada si aplica.
    try:
        return service.list_series()
    except Exception as e:
        return jsonify({"error": f"Error al listar series: {str(e)}"}), 500


@bp.post("/")
def create_series():
    """Crea una nueva serie."""
    payload = request.get_json(silent=True) or {}
    # ✅ TODO: usar service.create_series y devolver 201 con la nueva serie.
    try:
        return service.create_series(payload)
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error al crear serie: {str(e)}"}), 500


@bp.get("/<int:series_id>")
def retrieve_series(series_id: int):
    """Devuelve los detalles de una serie."""
    # ✅ TODO: invocar service.get_series y construir respuesta con temporadas.
    try:
        return service.get_series(series_id)
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error al recuperar serie: {str(e)}"}), 500


@bp.put("/<int:series_id>")
def update_series(series_id: int):
    """Actualiza la informacion de una serie."""
    payload = request.get_json(silent=True) or {}
    # ✅ TODO: invocar service.update_series y devolver la serie actualizada.
    try:
        return service.update_series(series_id, payload)
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error al actualizar serie: {str(e)}"}), 500


@bp.delete("/<int:series_id>")
def delete_series(series_id: int):
    """Elimina una serie del catalogo."""
    # ✅ TODO: invocar service.delete_series y devolver 204.
    try:
        return service.delete_series(series_id)
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error al eliminar serie: {str(e)}"}), 500


@bp.post("/<int:series_id>/seasons")
def add_season(series_id: int):
    """Agrega una temporada a una serie existente."""
    payload = request.get_json(silent=True) or {}
    # ✅ TODO: invocar service.add_season y devolver la temporada creada.
    try:
        return service.add_season(series_id, payload)
    except (BadRequest, NotFound) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error al crear temporada: {str(e)}"}), 500
