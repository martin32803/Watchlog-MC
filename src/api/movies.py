"""Endpoints relacionados con peliculas."""
from flask import Blueprint, jsonify, request
from src.extensions import db
from werkzeug.exceptions import NotFound, BadRequest

bp = Blueprint("movies", __name__, url_prefix="/movies")


class MovieService:
    """Orquesta la logica de negocio para el recurso Movie."""

    # ✅ TODO: inyectar dependencias necesarias (db.session, modelos, esquemas, etc.).
    def __init__(self):
        from src.models.movie import Movie
        self.Movie = Movie
        self.session = db.session

    def list_movies(self):
        """Retorna todas las peliculas registradas."""
        movies = self.Movie.query.all()
        movie_list = [movie.to_dict() for movie in movies]
        return jsonify(movie_list), 200

    def create_movie(self, payload: dict):
        """Crea una nueva pelicula."""
        # ✅ TODO: validar el payload y persistir un nuevo registro Movie.
        required_fields = ["title", "genre", "release_year"]

        # Validación básica
        if not all(field in payload for field in required_fields):
            raise BadRequest(f"Faltan campos requeridos: {', '.join(required_fields)}")

        # Crear nueva instancia
        new_movie = self.Movie(
            title=payload["title"],
            genre=payload["genre"],
            release_year=payload["release_year"],
        )

        self.session.add(new_movie)
        self.session.commit()

        return jsonify(new_movie.to_dict()), 201

    def get_movie(self, movie_id: int):
        """Obtiene una pelicula por su identificador."""
        # ✅ TODO: buscar la pelicula y manejar el caso de no encontrada.
        movie = self.Movie.query.get(movie_id)
        if not movie:
            raise NotFound(f"No se encontró la película con id {movie_id}")
        return jsonify(movie.to_dict()), 200

    def update_movie(self, movie_id: int, payload: dict):
        """Actualiza los datos de una pelicula."""
        # ✅ TODO: aplicar cambios permitidos y guardar en la base de datos.
        movie = self.Movie.query.get(movie_id)
        if not movie:
            raise NotFound(f"No se encontró la película con id {movie_id}")

        allowed_fields = ["title", "genre", "release_year"]
        for field in allowed_fields:
            if field in payload:
                setattr(movie, field, payload[field])

        self.session.commit()
        return jsonify(movie.to_dict()), 200

    def delete_movie(self, movie_id: int):
        """Elimina una pelicula existente."""
        # ✅ TODO: definir si el borrado debe ser logico o fisico.
        # Implementaremos borrado físico
        movie = self.Movie.query.get(movie_id)
        if not movie:
            raise NotFound(f"No se encontró la película con id {movie_id}")

        self.session.delete(movie)
        self.session.commit()
        return "", 204


# Instancia del servicio
service = MovieService()


@bp.get("/")
def list_movies():
    """Lista todas las peliculas disponibles."""
    return service.list_movies()


@bp.post("/")
def create_movie():
    """Crea una pelicula a partir de los datos enviados."""
    payload = request.get_json(silent=True) or {}

    try:
        return service.create_movie(payload)
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error al crear la película: {str(e)}"}), 500


@bp.get("/<int:movie_id>")
def retrieve_movie(movie_id: int):
    """Devuelve el detalle de una pelicula concreta."""
    try:
        return service.get_movie(movie_id)
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error al recuperar la película: {str(e)}"}), 500


@bp.put("/<int:movie_id>")
def update_movie(movie_id: int):
    """Actualiza la informacion de una pelicula."""
    payload = request.get_json(silent=True) or {}

    try:
        return service.update_movie(movie_id, payload)
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error al actualizar la película: {str(e)}"}), 500


@bp.delete("/<int:movie_id>")
def delete_movie(movie_id: int):
    """Elimina una pelicula del catalogo."""
    try:
        return service.delete_movie(movie_id)
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error al eliminar la película: {str(e)}"}), 500
