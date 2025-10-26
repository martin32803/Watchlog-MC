"""Modelo para usuarios que usan la plataforma."""
from datetime import datetime, timezone as ts

from src.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
#from .watch_entry import WatchEntry  # Importar WatchEntry para la relacion

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .watch_entry import WatchEntry  # Importar WatchEntry para la relacion

class User(db.Model):
    """Representa a un usuario (simulado mediante el header X-User-Id)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)  # id del usuario
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)  # nombre del usuario
    email: Mapped[str] = mapped_column(db.String(120), nullable=True)  # email del usuario
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(ts.utc))  # fecha de creacion
    watch_entries: Mapped[list["WatchEntry"]] = db.relationship()  # Relacion con WatchEntry (definida en WatchEntry)

    def __repr__(self) -> str:
        """Devuelve una representacion legible del usuario."""
        return f"<User id={getattr(self, 'id', None)} name={getattr(self, 'name', None)}>"

    def to_dict(self) -> dict:
        """Serializa al usuario para respuestas JSON."""
        return {
            "id": getattr(self, "id", None),
            "name": getattr(self, "name", None),
            "email": getattr(self, "email", None),
            "created_at": getattr(self, "created_at", datetime.utcnow()),
        }
