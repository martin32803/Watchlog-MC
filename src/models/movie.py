"""Modelo principal para las peliculas."""
from datetime import datetime, timezone

from src.extensions import db
from sqlalchemy.orm import Mapped, mapped_column

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .watch_entry import WatchEntry  # Importar WatchEntry para la relacion

# Mapped es utilizado para definir los tipos de las columnas del modelo.
# mapped_column se usa para configurar las propiedades de cada columna.
# Ver: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#declarative-mapping-using-typing-annotations
class Movie(db.Model):
    """Representa una pelicula dentro del catalogo."""
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)  # id de la pelicula
    title: Mapped[str] = mapped_column(db.String(120), nullable=False)  # titulo de la pelicula
    genre: Mapped[str] = mapped_column(db.String(50), nullable=False)  # genero de la pelicula
    release_year: Mapped[int] = mapped_column(nullable=False)  # ano de lanzamiento
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))  # fecha de creacion
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))  # fecha de actualizacion

    # cascade="all, delete-orphan" asegura que las entradas de watch_entry asociadas se eliminen si la pelicula se elimina
    # back_populates define la relacion inversa en WatchEntry
    # lazy='select' optimiza la carga de las entradas relacionadas
    watch_entries: Mapped[list['WatchEntry']] = db.relationship(
        "WatchEntry",
        cascade="all, delete-orphan",
        back_populates="movie",
        lazy='select'
    ) # Relacion con WatchEntry (definida en WatchEntry)

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
