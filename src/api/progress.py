"""Endpoints para controlar el progreso de los usuarios."""
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound
from src.extensions import db

bp = Blueprint("progress", __name__, url_prefix="")


class ProgressService:
    """Coordina operaciones sobre la lista de seguimiento y progreso."""

    # ✅ TODO: inyectar modelos User, Series, Movie y WatchEntry con sus esquemas.
    def __init__(self):
        from src.models.user import User
        from src.models.movie import Movie
        from src.models.serie import Serie
        from src.models.watch_entry import WatchEntry

        self.User = User
        self.Movie = Movie
        self.Serie = Serie
        self.WatchEntry = WatchEntry
        self.session = db.session

    def list_watchlist(self, user_id: int) -> list[dict]:
        """Devuelve los contenidos asociados a un usuario."""
        # ✅ TODO: consultar entradas filtradas por user_id y calcular porcentajes.
        user = self.User.query.get(user_id)
        if not user:
            raise NotFound(f"Usuario con id {user_id} no encontrado.")

        entries = self.WatchEntry.query.filter_by(user_id=user_id).all()
        result = [entry.to_dict() for entry in entries]
        return jsonify(result), 200

    def add_movie(self, user_id: int, movie_id: int) -> dict:
        """Agrega una pelicula a la lista del usuario."""
        # ✅ TODO: validar existencia del usuario y pelicula antes de crear el registro.
        user = self.User.query.get(user_id)
        if not user:
            raise NotFound(f"Usuario con id {user_id} no encontrado.")
        movie = self.Movie.query.get(movie_id)
        if not movie:
            raise NotFound(f"Película con id {movie_id} no encontrada.")

        # Verificar si ya existe
        existing = self.WatchEntry.query.filter_by(
            user_id=user_id, content_type="movie", content_id=movie_id
        ).first()
        if existing:
            raise BadRequest("La película ya está en la lista del usuario.")

        entry = self.WatchEntry(
            user_id=user_id,
            content_type="movie",
            content_id=movie_id,
            status="watching",
        )

        self.session.add(entry)
        self.session.commit()
        return jsonify(entry.to_dict()), 201

    def add_series(self, user_id: int, series_id: int) -> dict:
        """Agrega una serie a la lista del usuario."""
        # ✅ TODO: crear WatchEntry inicial con temporadas/episodios en cero.
        user = self.User.query.get(user_id)
        if not user:
            raise NotFound(f"Usuario con id {user_id} no encontrado.")
        serie = self.Serie.query.get(series_id)
        if not serie:
            raise NotFound(f"Serie con id {series_id} no encontrada.")

        existing = self.WatchEntry.query.filter_by(
            user_id=user_id, content_type="serie", content_id=series_id
        ).first()
        if existing:
            raise BadRequest("La serie ya está en la lista del usuario.")

        entry = self.WatchEntry(
            user_id=user_id,
            content_type="serie",
            content_id=series_id,
            status="watching",
            current_season=1,
            current_episode=1,
            watched_episodes=0,
            total_episodes=sum(s.episodes_count for s in serie.seasons) if serie.seasons else 0,
        )

        self.session.add(entry)
        self.session.commit()
        return jsonify(entry.to_dict()), 201

    def update_series_progress(self, user_id: int, series_id: int, payload: dict) -> dict:
        """Actualiza el progreso de una serie en la lista del usuario."""
        # ✅ TODO: validar limites de temporadas y episodios, recalcular porcentaje.
        entry = self.WatchEntry.query.filter_by(
            user_id=user_id, content_type="serie", content_id=series_id
        ).first()
        if not entry:
            raise NotFound(f"No hay registro de progreso para la serie {series_id} del usuario {user_id}.")

        serie = self.Serie.query.get(series_id)
        if not serie:
            raise NotFound(f"Serie con id {series_id} no encontrada.")

        total_episodes = sum(s.episodes_count for s in serie.seasons) if serie.seasons else 0
        entry.total_episodes = total_episodes

        if "watched_episodes" in payload:
            watched = int(payload["watched_episodes"])
            if watched < 0 or (total_episodes and watched > total_episodes):
                raise BadRequest("Número de episodios vistos fuera de rango.")
            entry.watched_episodes = watched

        if "current_season" in payload:
            entry.current_season = int(payload["current_season"])

        if "current_episode" in payload:
            entry.current_episode = int(payload["current_episode"])

        # Si completó todos los episodios
        if entry.watched_episodes == entry.total_episodes and entry.total_episodes > 0:
            entry.mark_as_watched()

        self.session.commit()
        return jsonify(entry.to_dict()), 200


# Instancia del servicio
service = ProgressService()


@bp.get("/me/watchlist")
def get_my_watchlist():
    """Devuelve la lista de seguimiento del usuario actual."""
    user_id = request.headers.get("X-User-Id", type=int)
    # ✅ TODO: validar el header y manejar autenticacion simulada.
    if not user_id:
        return jsonify({"error": "Falta el encabezado X-User-Id"}), 401

    try:
        return service.list_watchlist(user_id)
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error al obtener la watchlist: {str(e)}"}), 500


@bp.post("/watchlist/movies/<int:movie_id>")
def add_movie_to_watchlist(movie_id: int):
    """Agrega una pelicula a la lista del usuario."""
    user_id = request.headers.get("X-User-Id", type=int)
    # ✅ TODO: invocar service.add_movie y devolver 201 con la entrada creada.
    if not user_id:
        return jsonify({"error": "Falta el encabezado X-User-Id"}), 401

    try:
        return service.add_movie(user_id, movie_id)
    except (BadRequest, NotFound) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error al agregar película: {str(e)}"}), 500


@bp.post("/watchlist/series/<int:series_id>")
def add_series_to_watchlist(series_id: int):
    """Agrega una serie a la lista del usuario."""
    user_id = request.headers.get("X-User-Id", type=int)
    # ✅ TODO: invocar service.add_series y devolver 201 con la entrada creada.
    if not user_id:
        return jsonify({"error": "Falta el encabezado X-User-Id"}), 401

    try:
        return service.add_series(user_id, series_id)
    except (BadRequest, NotFound) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error al agregar serie: {str(e)}"}), 500


@bp.patch("/progress/series/<int:series_id>")
def update_series_progress(series_id: int):
    """Actualiza los datos de progreso de una serie."""
    user_id = request.headers.get("X-User-Id", type=int)
    payload = request.get_json(silent=True) or {}

    # ✅ TODO: invocar service.update_series_progress y devolver el recurso actualizado.
    if not user_id:
        return jsonify({"error": "Falta el encabezado X-User-Id"}), 401

    try:
        return service.update_series_progress(user_id, series_id, payload)
    except (BadRequest, NotFound) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error al actualizar progreso: {str(e)}"}), 500
