"""
Router pour la recherche avancée
"""

from fastapi import APIRouter, Depends, Query
from typing import Optional
from ..models.search import SearchQuery, SearchResponse
from ..services.search_service import SearchService
from ..dependencies import get_search_service

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get("/", response_model=SearchResponse)
async def search_persons(
    query: Optional[str] = Query(None, description="Recherche textuelle générale"),
    first_name: Optional[str] = Query(None, description="Prénom"),
    last_name: Optional[str] = Query(None, description="Nom de famille"),
    birth_year_min: Optional[int] = Query(None, ge=1000, le=2100),
    birth_year_max: Optional[int] = Query(None, ge=1000, le=2100),
    death_year_min: Optional[int] = Query(None, ge=1000, le=2100),
    death_year_max: Optional[int] = Query(None, ge=1000, le=2100),
    birth_place: Optional[str] = Query(None, description="Lieu de naissance"),
    death_place: Optional[str] = Query(None, description="Lieu de décès"),
    gender: Optional[str] = Query(None, pattern="^(M|F|U)$"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: SearchService = Depends(get_search_service)
):
    """
    Recherche avancée de personnes avec filtres multiples
    """
    search_query = SearchQuery(
        query=query,
        first_name=first_name,
        last_name=last_name,
        birth_year_min=birth_year_min,
        birth_year_max=birth_year_max,
        death_year_min=death_year_min,
        death_year_max=death_year_max,
        birth_place=birth_place,
        death_place=death_place,
        gender=gender,
        limit=limit,
        offset=offset
    )

    results = service.search(search_query)
    return results
