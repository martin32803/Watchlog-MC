"""Modelo puente que guarda el progreso del usuario."""
from datetime import datetime

from src.extensions import db


class WatchEntry(db.Model):
    """Relacion entre un usuario y un contenido (pelicula o serie)."""

    __tablename__ = "watch_entries"

    # TODO: definir columnas basicas (id, user_id, content_type, content_id, status).
    # TODO: agregar columnas de progreso (current_season, current_episode, watched_episodes, total_episodes).
    # TODO: establecer claves foraneas hacia User, Movie y Series segun el tipo.

    # TODO: modelar las relaciones back_populates con User, Movie y Series.

    def percentage_watched(self) -> float:
        """Calcula el porcentaje completado para el contenido asociado."""
        # TODO: implementar calculo utilizando watched_episodes y total_episodes.
        raise NotImplementedError("TODO: calcular porcentaje de avance real")

    def mark_as_watched(self) -> None:
        """Marca el contenido como completado."""
        # TODO: actualizar atributos y timestamps para reflejar el estado final.
        pass

    def to_dict(self) -> dict:
        """Serializa la entrada para respuestas JSON."""
        # TODO: reemplazar con serializacion acorde al modelo final.
        return {
            "id": getattr(self, "id", None),
            "user_id": getattr(self, "user_id", None),
            "content_type": getattr(self, "content_type", None),
            "content_id": getattr(self, "content_id", None),
            "status": getattr(self, "status", None),
            "current_season": getattr(self, "current_season", None),
            "current_episode": getattr(self, "current_episode", None),
            "watched_episodes": getattr(self, "watched_episodes", None),
            "total_episodes": getattr(self, "total_episodes", None),
            "updated_at": getattr(self, "updated_at", datetime.utcnow()),
        }
