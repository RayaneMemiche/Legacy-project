"""
Modèles Pydantic pour les personnes
"""

from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class PersonBase(BaseModel):
    """Modèle de base pour une personne"""

    first_name: str = Field(..., min_length=1, max_length=100, description="Prénom")
    last_name: str = Field(..., min_length=1, max_length=100, description="Nom de famille")
    birth_date: Optional[date] = Field(None, description="Date de naissance")
    birth_place: Optional[str] = Field(None, max_length=200, description="Lieu de naissance")
    death_date: Optional[date] = Field(None, description="Date de décès")
    death_place: Optional[str] = Field(None, max_length=200, description="Lieu de décès")
    gender: Optional[str] = Field(None, pattern="^(M|F|U)$", description="Genre (M/F/U)")
    occupation: Optional[str] = Field(None, max_length=200, description="Profession")
    notes: Optional[str] = Field(None, description="Notes additionnelles")


class PersonCreate(PersonBase):
    """Modèle pour la création d'une personne"""

    father_id: Optional[str] = Field(None, description="ID du père")
    mother_id: Optional[str] = Field(None, description="ID de la mère")


class PersonUpdate(BaseModel):
    """Modèle pour la mise à jour d'une personne"""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    birth_date: Optional[date] = None
    birth_place: Optional[str] = Field(None, max_length=200)
    death_date: Optional[date] = None
    death_place: Optional[str] = Field(None, max_length=200)
    gender: Optional[str] = Field(None, pattern="^(M|F|U)$")
    occupation: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None
    father_id: Optional[str] = None
    mother_id: Optional[str] = None


class PersonResponse(PersonBase):
    """Modèle de réponse pour une personne"""

    id: str = Field(..., description="Identifiant unique")
    father_id: Optional[str] = None
    mother_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PersonDetail(PersonResponse):
    """Modèle détaillé d'une personne avec relations"""

    father: Optional[PersonResponse] = None
    mother: Optional[PersonResponse] = None
    children: List[PersonResponse] = Field(default_factory=list)
    spouses: List[PersonResponse] = Field(default_factory=list)
    siblings: List[PersonResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
