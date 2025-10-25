"""Endpoints para controlar el progreso de los usuarios."""
from flask import Blueprint, jsonify, request

bp = Blueprint("progress", __name__, url_prefix="")


class ProgressService:
    """Coordina operaciones sobre la lista de seguimiento y progreso."""

    # TODO: inyectar modelos User, Series, Movie y WatchEntry con sus esquemas.

    def list_watchlist(self, user_id: int) -> list[dict]:
        """Devuelve los contenidos asociados a un usuario."""
        # TODO: consultar entradas filtradas por user_id y calcular porcentajes.
        pass

    def add_movie(self, user_id: int, movie_id: int) -> dict:
        """Agrega una pelicula a la lista del usuario."""
        # TODO: validar existencia del usuario y pelicula antes de crear el registro.
        pass

    def add_series(self, user_id: int, series_id: int) -> dict:
        """Agrega una serie a la lista del usuario."""
        # TODO: crear WatchEntry inicial con temporadas/episodios en cero.
        pass

    def update_series_progress(self, user_id: int, series_id: int, payload: dict) -> dict:
        """Actualiza el progreso de una serie en la lista del usuario."""
        # TODO: validar limites de temporadas y episodios, recalcular porcentaje.
        pass


service = ProgressService()


@bp.get("/me/watchlist")
def get_my_watchlist():
    """Devuelve la lista de seguimiento del usuario actual."""
    user_id = request.headers.get("X-User-Id", type=int)
    # TODO: validar el header y manejar autenticacion simulada.
    return (
        jsonify(
            {
                "detail": "TODO: implementar obtencion de watchlist",
                "user_id": user_id,
            }
        ),
        501,
    )


@bp.post("/watchlist/movies/<int:movie_id>")
def add_movie_to_watchlist(movie_id: int):
    """Agrega una pelicula a la lista del usuario."""
    user_id = request.headers.get("X-User-Id", type=int)
    # TODO: invocar service.add_movie y devolver 201 con la entrada creada.
    return (
        jsonify(
            {
                "detail": "TODO: implementar alta de pelicula en watchlist",
                "movie_id": movie_id,
                "user_id": user_id,
            }
        ),
        501,
    )


@bp.post("/watchlist/series/<int:series_id>")
def add_series_to_watchlist(series_id: int):
    """Agrega una serie a la lista del usuario."""
    user_id = request.headers.get("X-User-Id", type=int)
    # TODO: invocar service.add_series y devolver 201 con la entrada creada.
    return (
        jsonify(
            {
                "detail": "TODO: implementar alta de serie en watchlist",
                "series_id": series_id,
                "user_id": user_id,
            }
        ),
        501,
    )


@bp.patch("/progress/series/<int:series_id>")
def update_series_progress(series_id: int):
    """Actualiza los datos de progreso de una serie."""
    user_id = request.headers.get("X-User-Id", type=int)
    payload = request.get_json(silent=True) or {}
    # TODO: invocar service.update_series_progress y devolver el recurso actualizado.
    return (
        jsonify(
            {
                "detail": "TODO: implementar actualizacion de progreso",
                "series_id": series_id,
                "user_id": user_id,
                "payload_example": payload,
            }
        ),
        501,
    )
