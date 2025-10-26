"""Modelo puente que guarda el progreso del usuario."""
from datetime import datetime, timezone as tz

from src.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, foreign
from .user import User  # Importar User para la relacion
from typing import Optional
from .movie import Movie  # Importar Movie para la relacion
from .serie import Serie  # Importar Serie para la relacion
from sqlalchemy import and_


class WatchEntry(db.Model):
    """Relacion entre un usuario y un contenido (pelicula o serie)."""

    __tablename__ = "watch_entries"

    # TODO: definir columnas basicas (id, user_id, content_type, content_id, status).
    id: Mapped[int] = mapped_column(primary_key=True)  # id de la entrada
    content_type: Mapped[str] = mapped_column(db.String(20), nullable=False)  # tipo de contenido: 'movie' o 'serie'
    content_id: Mapped[int] = mapped_column(nullable=False)  # id del contenido (pelicula o serie)
    status: Mapped[str] = mapped_column(
        db.String(20),
        nullable=False,
        default="watching"
    )  # estado: 'watching', 'completed', 'on-hold', 'dropped', 'plan-to-watch'

    # TODO: agregar columnas de progreso (current_season, current_episode, watched_episodes, total_episodes).
    current_season: Mapped[Optional[int]] = mapped_column(nullable=True)  # temporada actual (para series)
    current_episode: Mapped[Optional[int]] = mapped_column(nullable=True)  # episodio actual (para series)
    watched_episodes: Mapped[Optional[int]] = mapped_column(nullable=True, default=0)  # episodios vistos (para series)
    total_episodes: Mapped[Optional[int]] = mapped_column(nullable=True)  # episodios totales (para series)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(tz.utc), onupdate=datetime.now(tz.utc))  # fecha de ultima actualizacion
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)  # id del usuario asociado

    # Relaciones
    user: Mapped[User] = db.relationship("User", back_populates="watch_entries")

    # Relaciones con Movie y Serie
    movie: Mapped[Optional['Movie']] = db.relationship(
        "Movie",
        back_populates="watch_entries",
        primaryjoin=lambda: and_(
            WatchEntry.content_type == 'movie',
            foreign(WatchEntry.content_id) == Movie.id,
        ),
        uselist=False,
        viewonly=True,
    )

    serie: Mapped[Optional['Serie']] = db.relationship(
        "Serie",
        back_populates="watch_entries",
        primaryjoin=lambda: and_(
            WatchEntry.content_type == 'serie',
            foreign(WatchEntry.content_id) == Serie.id,
        ),
        uselist=False,
        viewonly=True,
    )

    def percentage_watched(self) -> float:
        """Calcula el porcentaje completado para el contenido asociado."""
        return (self.watched_episodes / self.total_episodes * 100) if self.total_episodes else 0.0

    def mark_as_watched(self) -> None:
        """Marca el contenido como completado."""
        self.status = "completed"
        if self.content_type == "serie":
            self.current_season = None
            self.current_episode = None
            self.watched_episodes = self.total_episodes

    def to_dict(self) -> dict:
        """Serializa la entrada para respuestas JSON."""
        # TODO: reemplazar con serializacion acorde al modelo final.
        base_data = {
            "id": getattr(self, "id", None),
            "user_id": getattr(self, "user_id", None),
            "content_type": getattr(self, "content_type", None),
            "content_id": getattr(self, "content_id", None),
            "status": getattr(self, "status", None),
            "current_season": getattr(self, "current_season", None),
            "current_episode": getattr(self, "current_episode", None),
            "watched_episodes": getattr(self, "watched_episodes", None),
            "total_episodes": getattr(self, "total_episodes", None),
            "percentage_watched": round(self.percentage_watched(), 2),
            "updated_at": getattr(self, "updated_at", datetime.now(tz.utc)),
        }

        # Si es pelicula, agrega detalles del Movie
        if self.content_type == "movie" and self.movie:
            base_data["movie"] = self.movie.to_dict()

        # Si es serie, agrega detalles del Serie
        elif self.content_type == "serie" and self.serie:
            base_data["serie"] = self.serie.to_dict()

        return base_data
