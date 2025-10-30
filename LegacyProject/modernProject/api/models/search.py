"""
Modèles Pydantic pour la recherche
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from .person import PersonResponse


class SearchQuery(BaseModel):
    """Modèle de requête de recherche avancée"""

    query: Optional[str] = Field(None, description="Recherche textuelle générale")
    first_name: Optional[str] = Field(None, description="Prénom")
    last_name: Optional[str] = Field(None, description="Nom de famille")
    birth_year_min: Optional[int] = Field(None, ge=1000, le=2100, description="Année de naissance min")
    birth_year_max: Optional[int] = Field(None, ge=1000, le=2100, description="Année de naissance max")
    death_year_min: Optional[int] = Field(None, ge=1000, le=2100, description="Année de décès min")
    death_year_max: Optional[int] = Field(None, ge=1000, le=2100, description="Année de décès max")
    birth_place: Optional[str] = Field(None, description="Lieu de naissance")
    death_place: Optional[str] = Field(None, description="Lieu de décès")
    gender: Optional[str] = Field(None, pattern="^(M|F|U)$", description="Genre")
    limit: int = Field(100, ge=1, le=1000, description="Nombre max de résultats")
    offset: int = Field(0, ge=0, description="Offset pour pagination")


class SearchResponse(BaseModel):
    """Modèle de réponse de recherche"""

    total: int = Field(..., description="Nombre total de résultats")
    results: List[PersonResponse] = Field(..., description="Liste des résultats")
    limit: int
    offset: int
