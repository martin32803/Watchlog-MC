"""Modelo para series disponibles en el catalogo."""
from datetime import datetime as dt, timezone as t

from src.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .season import Season
    from .watch_entry import WatchEntry  # Importar WatchEntry para la relacion

class Serie(db.Model):
    """Representa una serie cargada por los usuarios."""

    __tablename__ = "serie"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    created_at: Mapped[dt] = mapped_column(default=dt.now(t.utc), nullable=False)
    updated_at: Mapped[dt] = mapped_column(
        default=dt.now(t.utc),
        onupdate=dt.now(t.utc),
        nullable=False,
    )
    
    # TODO: configurar relacion con Season (one-to-many) y WatchEntry.
    seasons: Mapped[List['Season']] = db.relationship()

    watch_entries: Mapped[List['WatchEntry']] = db.relationship(
        "WatchEntry",
        cascade="all, delete-orphan",
        back_populates="serie",
        lazy='select'
    )  # Relacion con WatchEntry (definida en WatchEntry)
    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        return f"<Series id={getattr(self, 'id', None)} title={getattr(self, 'title', None)}>"

    def to_dict(self, include_seasons: bool = False) -> dict:
        """Serializa la serie y opcionalmente sus temporadas."""
        # TODO: reemplazar por serializacion real usando marshmallow o similar.
        data = {
            "id": getattr(self, "id", None),
            "title": getattr(self, "title", None),
            "total_seasons": getattr(self, "total_seasons", None),
            "created_at": getattr(self, "created_at", dt.now(t.utc)),
        }
        if include_seasons:
            # TODO: serializar temporadas reales en lugar de lista vacia.
            data["seasons"] = []
        return data
