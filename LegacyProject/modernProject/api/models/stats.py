"""
Modèles Pydantic pour les statistiques
"""

from typing import Dict, List
from pydantic import BaseModel, Field


class CenturyDistribution(BaseModel):
    """Distribution par siècle"""

    century: str
    count: int


class NameDistribution(BaseModel):
    """Distribution par nom"""

    name: str
    count: int


class Statistics(BaseModel):
    """Modèle pour les statistiques générales"""

    total_persons: int = Field(..., description="Nombre total de personnes")
    total_families: int = Field(..., description="Nombre total de familles")
    total_males: int = Field(0, description="Nombre d'hommes")
    total_females: int = Field(0, description="Nombre de femmes")
    total_living: int = Field(0, description="Nombre de personnes vivantes")
    total_deceased: int = Field(0, description="Nombre de personnes décédées")
    oldest_birth_year: int | None = Field(None, description="Année de naissance la plus ancienne")
    newest_birth_year: int | None = Field(None, description="Année de naissance la plus récente")
    century_distribution: List[CenturyDistribution] = Field(default_factory=list)
    top_surnames: List[NameDistribution] = Field(default_factory=list)
    top_first_names: List[NameDistribution] = Field(default_factory=list)
    avg_children_per_family: float = Field(0.0, description="Moyenne d'enfants par famille")
    max_generations: int = Field(0, description="Nombre maximum de générations")
