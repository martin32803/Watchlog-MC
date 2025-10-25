"""Modelo que representa una temporada de una serie."""
from src.extensions import db

from sqlalchemy.orm import Mapped, mapped_column

class Season(db.Model):
    """Temporada asociada a una serie."""

    __tablename__ = "season"

    id: Mapped[int] = mapped_column(primary_key=True)  # id de la temporada
    series_id: Mapped[int] = mapped_column(db.ForeignKey("serie.id"), nullable=False)  # id de la serie asociada
    number: Mapped[int] = mapped_column(nullable=False)  # numero de la temporada
    episodes_count: Mapped[int] = mapped_column(nullable=False, default=0)  # cantidad de episodios en la temporada

    # TODO: establecer restriccion unica por (series_id, number).
    
    # TODO: configurar relacion back_populates con Series.
    # series = db.relationship("Series", back_populates="seasons")

    def to_dict(self) -> dict:
        """Serializa la temporada en un diccionario."""
        # TODO: reemplazar esta implementacion por la serializacion real.
        return {
            "id": getattr(self, "id", None),
            "series_id": getattr(self, "series_id", None),
            "number": getattr(self, "number", None),
            "episodes_count": getattr(self, "episodes_count", None),
        }
