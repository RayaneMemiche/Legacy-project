"""
Router pour les endpoints des familles
"""

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from ..models.family import FamilyCreate, FamilyUpdate, FamilyResponse
from ..services.family_service import FamilyService
from ..dependencies import get_family_service

router = APIRouter(
    prefix="/families",
    tags=["families"],
    responses={404: {"description": "Family not found"}},
)


@router.get("/", response_model=List[FamilyResponse])
async def get_all_families(
    skip: int = 0,
    limit: int = 100,
    service: FamilyService = Depends(get_family_service)
):
    """
    Récupérer toutes les familles avec pagination
    """
    families = service.get_all(skip=skip, limit=limit)
    return families


@router.get("/{family_id}", response_model=FamilyResponse)
async def get_family(
    family_id: str,
    service: FamilyService = Depends(get_family_service)
):
    """
    Récupérer les détails d'une famille par son ID
    """
    family = service.get_by_id(family_id)
    if not family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Family with id {family_id} not found"
        )
    return family


@router.post("/", response_model=FamilyResponse, status_code=status.HTTP_201_CREATED)
async def create_family(
    family: FamilyCreate,
    service: FamilyService = Depends(get_family_service)
):
    """
    Créer une nouvelle famille
    """
    try:
        new_family = service.create(family)
        return new_family
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{family_id}", response_model=FamilyResponse)
async def update_family(
    family_id: str,
    family: FamilyUpdate,
    service: FamilyService = Depends(get_family_service)
):
    """
    Mettre à jour une famille existante
    """
    updated_family = service.update(family_id, family)
    if not updated_family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Family with id {family_id} not found"
        )
    return updated_family


@router.delete("/{family_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_family(
    family_id: str,
    service: FamilyService = Depends(get_family_service)
):
    """
    Supprimer une famille
    """
    success = service.delete(family_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Family with id {family_id} not found"
        )
    return None
