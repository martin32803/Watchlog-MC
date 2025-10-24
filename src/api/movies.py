"""Endpoints relacionados con peliculas."""
from flask import Blueprint, jsonify, request

bp = Blueprint("movies", __name__, url_prefix="/movies")

class MovieService:
    """Orquesta la logica de negocio para el recurso Movie."""

    # TODO: inyectar dependencias necesarias (db.session, modelos, esquemas, etc.).
    def __init__(self):
        from src.models.movie import Movie  # noqa: F401
        self.Movie = Movie

    def list_movies(self) -> list[dict]:
        """Retorna todas las peliculas registradas."""
        movies = self.Movie.query.all()
        movie_list = []

        for movie in movies:
            movie_list.append(movie.to_dict())

        return jsonify(movie_list)

    def create_movie(self, payload: dict) -> dict:
        """Crea una nueva pelicula."""
        # TODO: validar el payload y persistir un nuevo registro Movie.
        pass

    def get_movie(self, movie_id: int) -> dict:
        """Obtiene una pelicula por su identificador."""
        # TODO: buscar la pelicula y manejar el caso de no encontrada.
        pass

    def update_movie(self, movie_id: int, payload: dict) -> dict:
        """Actualiza los datos de una pelicula."""
        # TODO: aplicar cambios permitidos y guardar en la base de datos.
        pass

    def delete_movie(self, movie_id: int) -> None:
        """Elimina una pelicula existente."""
        # TODO: definir si el borrado debe ser logico o fisico.
        pass


service = MovieService()


@bp.get("/")
def list_movies():
    """Lista todas las peliculas disponibles."""
    return service.list_movies(), 501


@bp.post("/")
def create_movie():
    """Crea una pelicula a partir de los datos enviados."""
    payload = request.get_json(silent=True) or {}
    # TODO: validar payload, manejar errores y devolver el recurso creado.
    return (
        jsonify(
            {
                "detail": "TODO: implementar creacion de pelicula",
                "payload_example": payload,
            }
        ),
        501,
    )


@bp.get("/<int:movie_id>")
def retrieve_movie(movie_id: int):
    """Devuelve el detalle de una pelicula concreta."""
    # TODO: invocar service.get_movie y manejar 404 cuando corresponda.
    return (
        jsonify(
            {
                "detail": "TODO: implementar recuperacion de pelicula",
                "movie_id": movie_id,
            }
        ),
        501,
    )


@bp.put("/<int:movie_id>")
def update_movie(movie_id: int):
    """Actualiza la informacion de una pelicula."""
    payload = request.get_json(silent=True) or {}
    # TODO: invocar service.update_movie y devolver el recurso actualizado.
    return (
        jsonify(
            {
                "detail": "TODO: implementar actualizacion de pelicula",
                "movie_id": movie_id,
                "payload_example": payload,
            }
        ),
        501,
    )


@bp.delete("/<int:movie_id>")
def delete_movie(movie_id: int):
    """Elimina una pelicula del catalogo."""
    # TODO: invocar service.delete_movie y devolver 204 al completar.
    return (
        jsonify(
            {
                "detail": "TODO: implementar borrado de pelicula",
                "movie_id": movie_id,
            }
        ),
        501,
    )
