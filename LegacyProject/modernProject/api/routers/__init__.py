"""
Routers de l'API
"""

from .persons import router as persons_router
from .families import router as families_router
from .auth import router as auth_router
from .search import router as search_router
from .stats import router as stats_router

__all__ = [
    "persons_router",
    "families_router",
    "auth_router",
    "search_router",
    "stats_router",
]
