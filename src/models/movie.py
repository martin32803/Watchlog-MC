"""Modelo principal para las peliculas."""
from datetime import datetime, timezone

from src.extensions import db

class Movie(db.Model):
    """Representa una pelicula dentro del catalogo."""

    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # TODO: crear relacion con WatchEntry (one-to-many) si aplica.

    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        return f"<Movie id={getattr(self, 'id', None)} title={getattr(self, 'title', None)}>"

    def to_dict(self) -> dict:
        """Serializa la instancia para respuestas JSON."""
        return {
            "id": getattr(self, "id", None),
            "title": getattr(self, "title", None),
            "genre": getattr(self, "genre", None),
            "release_year": getattr(self, "release_year", None),
            "created_at": getattr(self, "created_at", datetime.now(timezone.utc)),
            "updated_at": getattr(self, "updated_at", datetime.now(timezone.utc)),
        }
