"""
Modèles Pydantic pour les familles
"""

from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class FamilyBase(BaseModel):
    """Modèle de base pour une famille"""

    father_id: str = Field(..., description="ID du père")
    mother_id: str = Field(..., description="ID de la mère")
    marriage_date: Optional[date] = Field(None, description="Date de mariage")
    marriage_place: Optional[str] = Field(None, max_length=200, description="Lieu de mariage")
    divorce_date: Optional[date] = Field(None, description="Date de divorce")
    notes: Optional[str] = Field(None, description="Notes")


class FamilyCreate(FamilyBase):
    """Modèle pour la création d'une famille"""

    children_ids: Optional[List[str]] = Field(default_factory=list, description="IDs des enfants")


class FamilyUpdate(BaseModel):
    """Modèle pour la mise à jour d'une famille"""

    marriage_date: Optional[date] = None
    marriage_place: Optional[str] = Field(None, max_length=200)
    divorce_date: Optional[date] = None
    notes: Optional[str] = None
    children_ids: Optional[List[str]] = None


class FamilyResponse(FamilyBase):
    """Modèle de réponse pour une famille"""

    id: str = Field(..., description="Identifiant unique")
    children_ids: List[str] = Field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
