"""
Router pour les endpoints des personnes
"""

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from ..models.person import PersonCreate, PersonUpdate, PersonResponse, PersonDetail
from ..services.person_service import PersonService
from ..dependencies import get_person_service

router = APIRouter(
    prefix="/persons",
    tags=["persons"],
    responses={404: {"description": "Person not found"}},
)


@router.get("/", response_model=List[PersonResponse])
async def get_all_persons(
    skip: int = 0,
    limit: int = 100,
    service: PersonService = Depends(get_person_service)
):
    """
    Récupérer toutes les personnes avec pagination
    """
    persons = service.get_all(skip=skip, limit=limit)
    return persons


@router.get("/{person_id}", response_model=PersonDetail)
async def get_person(
    person_id: str,
    service: PersonService = Depends(get_person_service)
):
    """
    Récupérer les détails d'une personne par son ID
    """
    person = service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {person_id} not found"
        )
    return person


@router.post("/", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
async def create_person(
    person: PersonCreate,
    service: PersonService = Depends(get_person_service)
):
    """
    Créer une nouvelle personne
    """
    try:
        new_person = service.create(person)
        return new_person
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{person_id}", response_model=PersonResponse)
async def update_person(
    person_id: str,
    person: PersonUpdate,
    service: PersonService = Depends(get_person_service)
):
    """
    Mettre à jour une personne existante
    """
    updated_person = service.update(person_id, person)
    if not updated_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {person_id} not found"
        )
    return updated_person


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person(
    person_id: str,
    service: PersonService = Depends(get_person_service)
):
    """
    Supprimer une personne
    """
    success = service.delete(person_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {person_id} not found"
        )
    return None


@router.get("/{person_id}/ancestors", response_model=List[PersonResponse])
async def get_ancestors(
    person_id: str,
    generations: int = 4,
    service: PersonService = Depends(get_person_service)
):
    """
    Récupérer les ancêtres d'une personne
    """
    ancestors = service.get_ancestors(person_id, generations)
    if ancestors is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {person_id} not found"
        )
    return ancestors


@router.get("/{person_id}/descendants", response_model=List[PersonResponse])
async def get_descendants(
    person_id: str,
    generations: int = 4,
    service: PersonService = Depends(get_person_service)
):
    """
    Récupérer les descendants d'une personne
    """
    descendants = service.get_descendants(person_id, generations)
    if descendants is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {person_id} not found"
        )
    return descendants
