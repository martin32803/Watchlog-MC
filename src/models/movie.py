"""Modelo principal para las peliculas."""
from datetime import datetime, timezone

from src.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
# Mapped es utilizado para definir los tipos de las columnas del modelo.
# mapped_column se usa para configurar las propiedades de cada columna.
# Ver: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#declarative-mapping-using-typing-annotations
class Movie(db.Model):
    """Representa una pelicula dentro del catalogo."""

    id: Mapped[int] = mapped_column(primary_key=True)  # id de la pelicula
    title: Mapped[str] = mapped_column(db.String(120), nullable=False)  # titulo de la pelicula
    genre: Mapped[str] = mapped_column(db.String(50), nullable=False)  # genero de la pelicula
    release_year: Mapped[int] = mapped_column(nullable=False)  # ano de lanzamiento
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))  # fecha de creacion
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))  # fecha de actualizacion

    # TODO: crear relacion con WatchEntry (one-to-many) si aplica.
    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        return f"<Movie id={getattr(self, 'id', None)} title={getattr(self, 'title', None)} genre={getattr(self, 'genre', None)} release_year={getattr(self, 'release_year', None)}>"

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
