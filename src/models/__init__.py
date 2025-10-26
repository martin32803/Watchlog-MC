"""Coleccion de modelos disponibles en la aplicacion."""

# TODO: exponer nuevos modelos cuando se creen.
from .movie import Movie  # noqa: F401
from .season import Season  # noqa: F401
from .serie import Serie  # noqa: F401
from .user import User  # noqa: F401
from .watch_entry import WatchEntry  # noqa: F401

__all__ = ["Movie", "Season", "Serie", "User", "WatchEntry"]
